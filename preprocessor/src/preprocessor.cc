#include "preprocessor.h"

#include <sstream>
#include <iostream>
#include <vector>
#include <unordered_map>
#include <cctype>


const std::unordered_map<Preprocessor::DFAState, std::unordered_map<Preprocessor::CharType, Preprocessor::DFAState>> Preprocessor::dfa = 
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

Preprocessor::Cmd::Cmd(const CmdType type, const std::string targetsStr): type{type}
{
	// Split the string targets by spaces but keeping quoted strings together
	DFAState state = DFAState::START;
	int startIdx = 0;

	for (int i = 0; i < targetsStr.length(); i++)
	{
		CharType type;
		if (targetsStr[i] == '"') // QUOTE
		{	
			type = CharType::QUOTE;
		}
		else if (isspace(targetsStr[i]))
		{
			type = CharType::WHITESPACE;
		}
		else
		{
			type = CharType::OTHER;
		}

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

Preprocessor::Preprocessor(std::unordered_map<std::string, std::unique_ptr<File>> &fl): 
fileList{move(fl)}
{

}

void Preprocessor::build()
{

}

void Preprocessor::build(const std::string &noteName)
{

}

Preprocessor::Cmd Preprocessor::getCmd(const std::string &rawCommand)
{
	std::size_t pos = rawCommand.find('(');
	std::string partialCmd = rawCommand.substr(pos + 1, rawCommand.length() - pos - 2);
	bool seenCmd = false;
	int cmdLen = -1;

	for (int i = 0; i < partialCmd.length(); i++)
	{
		if ( isspace(partialCmd[i]) && seenCmd) 
		{
			cmdLen = i;
			break;
		}
		else if (!isspace(partialCmd[i]))
		{
			seenCmd = true;
		}
	}

	return Preprocessor::Cmd(strToCmdType(partialCmd.substr(0, cmdLen)), partialCmd.substr(cmdLen, partialCmd.length() - cmdLen));
}

Preprocessor::CmdType Preprocessor::strToCmdType(const std::string &str)
{
	if (str == "include") { return Preprocessor::CmdType::INCLUDE; }
	else if (str == "link") { return Preprocessor::CmdType::LINK; }
	else if (str == "nobuild") { return Preprocessor::CmdType::NOBUILD; }

	return Preprocessor::CmdType::ERR;
}