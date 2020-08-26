#ifndef PREPROCESSOR_H
#define PREPROCESSOR_H

#include "file.h"

#include <regex>
#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <memory>


class Preprocessor 
{
	
public:
	enum CmdType { INCLUDE = 0, LINK, NOBUILD, ERR };
	enum DFAState { START = 0, LEADINGWS, STARTQUOTE, MIDQUOTE, ENDQUOTE, MIDNORM, ERROR };
	enum CharType { WHITESPACE = 0, QUOTE, OTHER };

private:
	// Store a list of files to preprocess
	std::unordered_map<std::string, std::unique_ptr<File>> fileList;

	// Store a cache of files that already have been processed - indicate 
	std::unordered_set<File*> cache;

	static const std::unordered_map<DFAState, std::unordered_map<CharType, DFAState>>  dfa;

public:

	class Cmd 
	{
		CmdType type;
		std::vector<std::string> targets;

	public:
		Cmd(const CmdType type, const std::string targetsStr);
		
		CmdType getType() { return type; }
		const std::vector<std::string> &getTargets() { return targets; }

		bool operator==(const CmdType otherType) { return type == otherType; }
	};

	// Force the argument to be moved in 
	Preprocessor(std::unordered_map<std::string, std::unique_ptr<File>> &filesToProcess);

	// Build designated file recursively
	void build (const std::string &noteName);
	
	// Build the next nonvisited file in the file list
	void build ();

	static Cmd getCmd(const std::string &rawCommand);

	static CmdType strToCmdType(const std::string &);
	
};

#endif