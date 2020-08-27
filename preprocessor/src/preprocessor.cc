#include "preprocessor.h"

#include <fstream>
#include <iostream>
#include <vector>
#include <unordered_map>
#include <cctype>
#include <sys/stat.h>
#include <sys/types.h>
#include <regex>

using namespace std;

const unordered_map<Preprocessor::DFAState, unordered_map<Preprocessor::CharType, Preprocessor::DFAState>> Preprocessor::dfa = 
{
	{ DFAState::START, 
		{
			{ CharType::OTHER, DFAState::MIDNORM }, 
			{ CharType::WHITESPACE, DFAState::LEADINGWS },
			{ CharType::QUOTE, DFAState::STARTQUOTE }
		}
	},
	{ DFAState::LEADINGWS, 
		{
			{ CharType::OTHER, DFAState::MIDNORM },
			{ CharType::WHITESPACE, DFAState::LEADINGWS },
			{ CharType::QUOTE, DFAState::STARTQUOTE }
		}
	},
	{ DFAState::STARTQUOTE, 
		{
			{ CharType::OTHER, DFAState::MIDQUOTE },
			{ CharType::WHITESPACE, DFAState::MIDQUOTE },
			{ CharType::QUOTE, DFAState::START }
		}
	},
	{ DFAState::MIDQUOTE, 
		{
			{ CharType::OTHER, DFAState::MIDQUOTE },
			{ CharType::WHITESPACE, DFAState::MIDQUOTE },
			{ CharType::QUOTE, DFAState::ENDQUOTE }
		}
	},
	{ DFAState::ENDQUOTE, 
		{
			{ CharType::OTHER, DFAState::ERROR },
			{ CharType::WHITESPACE, DFAState::START },
			{ CharType::QUOTE, DFAState::ERROR }
		}
	},
	{ DFAState::MIDNORM, 
		{
			{ CharType::OTHER, DFAState::MIDNORM },
			{ CharType::WHITESPACE, DFAState::START },
			{ CharType::QUOTE, DFAState::MIDNORM }
		}
	}
};

Preprocessor::Cmd::Cmd(const CmdType type, const string targetsStr): type{type}
{
	// Split the string targets by spaces but keeping quoted strings together
	DFAState state = DFAState::START;
	int startIdx = 0;

	for (int i = 0; i < targetsStr.length(); i++)
	{
		CharType type;
		if (targetsStr[i] == '"') {	type = CharType::QUOTE;	}
		else if (isspace(targetsStr[i])) { type = CharType::WHITESPACE;	}
		else { type = CharType::OTHER; }

		const DFAState pstate = state;
		state = dfa.at(state).at(type); // Step to next state

		if (state == DFAState::START && pstate == DFAState::ENDQUOTE) 
		{
			targets.emplace_back(targetsStr.substr(startIdx, i-startIdx - 1)); // Remove the quotes from the argument
		}
		else if (state == DFAState::START && pstate == DFAState::MIDNORM)
		{
			targets.emplace_back(targetsStr.substr(startIdx, i-startIdx));
		}
		else if (state == DFAState::STARTQUOTE)
		{
			startIdx = i+1;
		}
		else if (state == DFAState::MIDNORM && pstate != DFAState::MIDNORM) 
		{
			startIdx = i;
		}
	}

	if (state == DFAState::MIDNORM) // Emit final token if necessary
	{
		targets.emplace_back(targetsStr.substr(startIdx, targetsStr.length() - startIdx));
	} 
	else if (state == DFAState::ENDQUOTE)
	{
		targets.emplace_back(targetsStr.substr(startIdx, targetsStr.length() - startIdx - 1));
	}
}

// ------------------- PREPROCESSOR -----------------------

Preprocessor::Preprocessor(unordered_map<string, unique_ptr<File>> fl, const string notesDir): 
fileList{move(fl)}, baseNotesDir{move(notesDir)} {}

// API Build function
void Preprocessor::build()
{
	cerr << "Initiating build..." << endl;
	// Setup the build directory 

	int status = mkdir((baseNotesDir + "/build").c_str(), S_IRWXU);
	status = mkdir((baseNotesDir + "/build/.flat_notes").c_str(), S_IRWXU);

	// Loop over not visited notes
	auto itr = fileList.begin();
	File *file = itr->second.get();
	
	while (!file->isVisited())
	{
		build(file->getName());
		file = file->getNext();
	}

	linkBuiltFiles();
}

// NoBuild simply means do not make any copies out of flat notes in builddir
void Preprocessor::build(const string &noteName)
{
	File *note = fileList[noteName].get();
	if (shouldShortCircuit(note)) { return; }
	
	cerr << "Initializing build of " << noteName << std::endl;

	static basic_regex pattern("\\[\\/\\/\\]\\s*:\\s*#\\s*\\(.*\\)");
	
	note->visit();
	ifstream in (baseNotesDir + "/.flat_notes/" + note->getName());
	ofstream out (baseNotesDir + "/build/.flat_notes/" + note->getName());
	smatch matchRes;
	string line;

	while (getline(in, line))
	{
		bool foundMatch = regex_search(line, matchRes, pattern);
		if (!foundMatch)
		{
			out << line << "\n";
		}
		else 
		{
			for (int i = 0; i < matchRes.size(); ++i)
			{
				Cmd cmd = getCmd(matchRes[i]);
				applyCmd(cmd, note, out);
			}
		}
	}

	out << flush;
	cache.emplace(note); // Add the note to the cache as it is done building
}

void Preprocessor::linkBuiltFiles()
{
	cerr << "Linking..." << endl;
	// Copy over all other filters to build but use /build versions of the notes
	// Only copy over if willBuild is true for the file

}

bool Preprocessor::shouldShortCircuit(File *note)
{
	bool isCached = cache.find(note) != cache.end();

	if (isCached) { return true; }
	else if (note->isVisited()) 
	{
		cerr << "[ ERROR ]: Cyclic dependancy detected. Exiting." << endl;
		return true;
	}
	return false;

}

void Preprocessor::applyCmd(const Cmd &cmd, File *curFile, ostream &curFileStream)
{
	switch (cmd.getType()) 
	{
		case CmdType::INCLUDE:
		{
			const auto & targets = cmd.getTargets();
			for (const auto &target : targets)
			{
				build(target); // Recursively build each target to include in order
				// Copy build contents into the current file inline
				copyBuiltFile(curFileStream, target);
			}
			break;
		}
		case CmdType::LINK:
			break;
		case CmdType::NOBUILD:
			curFile->setNoBuild();
			break;
		case CmdType::ERR:
			cerr << "[ WARN ]: Command not recognized, ignoring." << endl;
			break;	
	}
}

void Preprocessor::copyBuiltFile(ostream &curFileStream, const string &srcName)
{
	// append the contents of the built note with name noteToAppend to the currentFileStream
	ifstream source (baseNotesDir + "/build/.flat_notes/" + srcName);
	curFileStream << source.rdbuf(); // send the entire contents of source
}

Preprocessor::Cmd Preprocessor::getCmd(const string &rawCommand)
{
	size_t pos = rawCommand.find('(');
	string partialCmd = rawCommand.substr(pos + 1, rawCommand.length() - pos - 2);
	bool seenCmd = false;
	int cmdLen = -1;

	for (int i = 0; i < partialCmd.length(); i++)
	{
		if (isspace(partialCmd[i]) && seenCmd) 
		{
			cmdLen = i;
			break;
		}
		else if (!isspace(partialCmd[i]))
		{
			seenCmd = true;
		}
	}

	const string targets = (cmdLen < partialCmd.length() && cmdLen > 0) ? partialCmd.substr(cmdLen, partialCmd.length() - cmdLen) : "";

	return Cmd(strToCmdType(partialCmd.substr(0, cmdLen)), targets);
}

Preprocessor::CmdType Preprocessor::strToCmdType(const string &str)
{
	if (str == "include") { return CmdType::INCLUDE; }
	else if (str == "link") { return CmdType::LINK; }
	else if (str == "nobuild") { return CmdType::NOBUILD; }

	return CmdType::ERR;
}