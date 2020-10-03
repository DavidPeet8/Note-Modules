#include "preprocessor.h"
#include "file.h"
#include "command.h"
#include "logger.h"

#include <fstream>
#include <iostream>
#include <vector>
#include <unordered_map>
#include <cctype>
#include <sys/stat.h>
#include <sys/types.h>
#include <regex>
#include <filesystem>
#include <functional>

using namespace std;
namespace fs = std::filesystem;


// ------------------- PREPROCESSOR -----------------------

Preprocessor::Preprocessor(unordered_map<string, unique_ptr<File>> &fl, const string notesDir): 
fileList{fl}, baseNotesDir{move(notesDir)} 
{}

// API Build function
void Preprocessor::build()
{
	Logger::info() << "Initiating build ...\n";
	// Setup the build directory 

	int status = mkdir((baseNotesDir + "/build").c_str(), S_IRWXU);
	status = mkdir((baseNotesDir + "/build/.flat_notes").c_str(), S_IRWXU);

	// Loop over not visited notes
	File *file = fileList.begin()->second.get();
	
	while (!file->isVisited())
	{
		Logger::info() << "Starting build for " << file->getName() << "\n";
		build(file->getName());
		file = file->getNext();
	}

	Logger::info() << "Build completed, Initiating linking step\n";
	linkBuiltFiles(fs::absolute(baseNotesDir), ""); // Must pass absolute path
}

// Add to the list of files that we will preprocess
void Preprocessor::addToFilesList(unordered_map<string, unique_ptr<File>>::iterator &itr, const string &noteName)
{
	File *prevFile = fileList.begin()->second.get();
	File *nextFile = prevFile->getNext();

	// Not in the file list but on the file system
	itr = fileList.emplace(noteName, make_unique<File>(noteName)).first;

	itr->second->setPrev(prevFile); // Set current to point to previous node
	itr->second->setNext(nextFile); // Set current to point to next node
	prevFile->setNext(itr->second.get()); // Set previous to point to new node
	nextFile->setPrev(itr->second.get()); // Set next to point back to current node
}

// NoBuild simply means do not make any copies out of flat notes in builddir
void Preprocessor::build(const string &noteName)
{
	using namespace std::placeholders;

	auto itr = fileList.find(noteName);
	if (itr == fileList.end() && fs::exists(baseNotesDir + "/.flat_notes/" + noteName)) 
	{
		addToFilesList(itr, noteName);
	}
	else if (itr == fileList.end())
	{
		Logger::err() << "Note with name " << noteName << " does not exist and cannot be built\n";
		return;
	}

	File *note = itr->second.get();
	if (shouldShortCircuit(note)) 
	{
		Logger::info() << "File is cached and already built, skipping.\n";
		return; 
	}
	Logger::info() << noteName << " is not cached, building now\n";

	static basic_regex pattern("<!--.*?-->");
	
	note->visit(); // Visit the node and remove it from the linked list of unvisited files
	ifstream in (baseNotesDir + "/.flat_notes/" + note->getName());
	ofstream out (baseNotesDir + "/build/.flat_notes/" + note->getName());
	string line = "";

	while (getline(in, line))
	{
		// Use regex iterator here?
		const auto matchBeginItr = sregex_iterator(line.begin(), line.end(), pattern);
		const auto matchEndItr = sregex_iterator();
		const char * end = isBoldColonCase(line) ? "\n\n" : "  \n";

		if (matchBeginItr == matchEndItr)
		{
			out << line << end;
			continue;
		}

		// Loop over all matches found in this line
		for (auto match = matchBeginItr; match != matchEndItr; ++match)
		{
			string matchedStr = match->str();
			out << match->prefix();
			vector<Cmd> cmds = Cmd::getCmds(matchedStr);

			for (const auto &cmd : cmds)
			{
				Cmd::CommandHandlers handlers = {
					std::bind(&Preprocessor::includeHandler, this, note, ref(out), _1),
					std::bind(&Preprocessor::linkHandler, this, note, ref(out), _1), 
					std::bind(&Preprocessor::nobuildHandler, this, note, ref(out), _1),
					std::bind(&Preprocessor::imgHandler, this, note, ref(out), _1),
					std::bind(&Preprocessor::errHandler, this, note, ref(out), _1)
				};
				cmd.apply(handlers);
			}
			if (match == matchEndItr) { out << match->suffix() << end; }
		}
	}

	out << flush;
	cache.emplace(note); // Add the note to the cache as it is done building
}

void Preprocessor::linkBuiltFiles(const string &basePath, const string &pathTail)
{
	// Traversal over non-hidden folders recreating folder and file structure
	const auto cwd = fs::current_path();
	fs::current_path(baseNotesDir + pathTail); // cd into build directory
	fs::directory_iterator baseDir(basePath + pathTail);

	for (const auto &item : baseDir)
	{
		string name = item.path().filename().string();
		// cerr << "Linking " << name << endl;
		string mirrorPath = basePath + "/build" + pathTail + "/" + name;

		if (name[0] == '.' || name == "build") { continue; }
		if (item.is_directory())
		{
			// Create the corresponding directory under 
			if (!fs::exists(mirrorPath))
			{
				Logger::info() << "Directory created: " << mirrorPath << "\n";
				fs::create_directory(mirrorPath);
			}
			linkBuiltFiles(basePath, pathTail + "/" + name); // Recursively process next dir
		}
		else if (item.is_regular_file())
		{
			if (fs::exists(mirrorPath)) { fs::remove(mirrorPath); }

			const auto itr = fileList.find(name);

			if (fs::exists(basePath + "/build/.flat_notes/" + name) && itr != fileList.end() && itr->second->shouldBuild()) 
			{
				fs::create_hard_link(basePath + "/build/.flat_notes/" + name, mirrorPath);
			}
		}
	}

	fs::current_path(cwd);
}

bool Preprocessor::shouldShortCircuit(File *note)
{
	bool isCached = cache.find(note) != cache.end();

	if (isCached) { return true; }
	else if (note->isVisited()) 
	{
		Logger::err() << "Cyclic dependancy detected. Exiting.\n";
		return true;
	}
	return false;

}

const string Preprocessor::getLinkPath(const string &target)
{
	// This is horrible I should really fix this
	return string("/Note-Modules/#/note/build/.flat_notes/") + string(fs::path(target).filename());
}

void Preprocessor::copyBuiltFile(ostream &curFileStream, const string &srcName)
{
	// append the contents of the built note with name noteToAppend to the currentFileStream
	ifstream source (baseNotesDir + "/build/.flat_notes/" + srcName);
	curFileStream << source.rdbuf(); // send the entire contents of source
}

// There is a strange edge case where "  \n" does not create a line break if we have "**boldtxt**:  \n"
bool Preprocessor::isBoldColonCase(const string &line)
{
	const string pattern = "**:";
	return line.length() > 3 && line.compare(line.length() - 3, 3, pattern) == 0;
}

void Preprocessor::includeHandler(File * const curFile, ostream &curFileStream, const vector<string> &targets)
{
	curFileStream << "\n";
	for (const auto &target : targets)
	{
		Logger::info() << "Recursively Building target " << target << "\n";
		build(target); // Recursively build each target to include in order
		// Copy build contents into the current file inline
		copyBuiltFile(curFileStream, target);
	}
}

void Preprocessor::linkHandler(File * const curFile, ostream &curFileStream, const vector<string> &targets)
{
	// Here we print out the proper link
	for (const auto &target : targets)
	{
		curFileStream << " [" << fs::path(target).filename() << "]" << "(" << getLinkPath(target) << ") "; 
	}
}

void Preprocessor::nobuildHandler(File * const curFile, ostream &curFileStream, const vector<string> &targets)
{
	curFile->setNoBuild();
}

void Preprocessor::errHandler(File * const curFile, ostream &curFileStream, const vector<string> &targets)
{
	Logger::warn() << "Command not recognized, ignoring.\n";
}

void Preprocessor::imgHandler(File * const curFile, ostream &curFileStream, const vector<string> &targets)
{
	curFileStream << "\n<div class=\"md-img-container\">";
	for (const auto &target : targets)
	{
		curFileStream << "<img class=\"md-img\" src=\"" << makeURL(target) << "\"/>";
	}
	curFileStream << "</div>\n";
}

const string Preprocessor::makeURL(const string &target)
{
	static basic_regex pattern("https?://.*?");

	const auto matchBeginItr = sregex_iterator(target.begin(), target.end(), pattern);
	const auto matchEndItr = sregex_iterator();

	if (matchBeginItr == matchEndItr)
	{
		// Assume you are reffering to a local file
		return string("http://localhost:8000/image/") + target;
	} 
	else 
	{
		// Assume that you put in a url properly
		return target;
	}
}