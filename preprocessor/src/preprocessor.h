#ifndef PREPROCESSOR_H
#define PREPROCESSOR_H

#include <regex>
#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>

class File;

class Preprocessor 
{
	enum CmdTypes { INCLUDE, LINK, NOBUILD, ERR };

	class Cmd 
	{
		CmdTypes type;
		std::vector<std::string> targets;

	public:
		Cmd(const CmdTypes type, const std::string targetsStr);
		CmdTypes getType() { return type; }

		bool operator==(const CmdTypes otherType) { return type == otherType; }
	};

	// Store a list of files to preprocess
	std::unordered_map<std::string, std::unique_ptr<File>> fileList;

	// Store a cache of files that already have been processed - indicate 
	std::unordered_set<File*> cache;

public:
	// Force the argument to be moved in 
	Preprocessor(std::unordered_map<std::string, std::unique_ptr<File>> &&filesToProcess);

	// Build designated file recursively
	void build (const std::string &noteName);
	
	// Build the next nonvisited file in the file list
	void build ();

	Cmd getCmd(const std::string &rawCommand);

private:
	CmdTypes strToCmdType(const std::string &);
	
};

#endif