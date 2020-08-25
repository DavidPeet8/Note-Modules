#include "preprocessor.h"

#include <sstream>

Preprocessor::Cmd::Cmd(const CmdTypes type, const std::string targetsStr)
{
	// Split the string targets by spaces but keeping quoted strings together
	int startIdx = 0;
	bool seenWord = false;
	bool inQuotedArg = false;

	for (int i = 0; i < targetsStr.length(); i++)
	{
		if (targets[i] == " " && !inQuotedArg && seenWord) 
		{
			// End Idx is exclusive
			targets.emplace_back(targetsStr.substr(startIdx, i));
			startIdx = i+1;
			seenWord = false;
		} 
		else if (!seenWord && targets[i] == " ")
		{
			// multiple consecutive spaces, ignorebut increment starting index
			startIdx = i+1;
		}
		else if (targets[i] == "\"") 
		{
			inQuotedArg = !inQuotedArg; // Flip weather we are in a quoted argument
			
			if (!inQuotedArg) 
			{
				targets.emplace_back(targetsStr.substr(startIdx, i));
				startIdx = i+1;
				seenWord = false;
			}
		}
		else
		{
			seenWord = true;
		}
	}
}

// ------------------- PREPROCESSOR -----------------------

Preprocessor::Preprocessor(std::unordered_map<std::string, std::unique_ptr<File>> &&fileList): 
fileList{fileList}
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
	std::string partialCmd = rawCommand.substr(pos + 1, rawCommand.length() - 1);
	std::istringstream iss(partialCmd);
	std::string cmd; 
	iss >> cmd;

	return Preprocessor::Cmd(strToCmdType(cmd), iss.str());
}

Preprocessor::CmdTypes Preprocessor::strToCmdType(const std::string &str)
{
	if (str == "include") { return Preprocessor::CmdTypes::INCLUDE; }
	else if (str == "link") { return Preprocessor::CmdTypes::LINK; }
	else if (str == "nobuild") { return Preprocessor::CmdTypes::NOBUILD; }

	return Preprocessor::CmdTypes::ERR;
}