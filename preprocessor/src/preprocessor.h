#ifndef PREPROCESSOR_H
#define PREPROCESSOR_H

#include "file.h"

#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <memory>
#include <regex>


class Preprocessor 
{
	
public:
	enum CmdType { INCLUDE = 0, LINK, NOBUILD, IMG, ERR };
	enum DFAState { START = 0, LEADINGWS, STARTQUOTE, MIDQUOTE, ENDQUOTE, MIDNORM, ERROR };
	enum CharType { WHITESPACE = 0, QUOTE, OTHER };

private:
	// Store a list of files to preprocess
	std::unordered_map<std::string, std::unique_ptr<File>> fileList;
	const std::string baseNotesDir;

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

		CmdType getType() const { return type; }
		const std::vector<std::string> &getTargets() const { return targets; }

	};

	// Force the argument to be moved in 
	Preprocessor(std::unordered_map<std::string, std::unique_ptr<File>> filesToProcess, const std::string baseNotesDir);
	
	// Build the next nonvisited file in the file list
	void build ();

	static std::vector<Cmd> getCmds(const std::string &rawCommand);

	static CmdType strToCmdType(const std::string &);
	static std::string cmdTypeToStr(const CmdType);

private:
	// Build designated file recursively
	void build (const std::string &noteName);

	void linkBuiltFiles(const std::string &basePath, const std::string &pathTail = "");

	void applyCmd(const Cmd &cmd, File *curFile, std::ostream &);

	void copyBuiltFile(std::ostream &curFileStream, const std::string &noteToAppend);
	
	bool shouldShortCircuit(File *note);

	bool isBoldColonCase(const std::string &line);

	void addToFilesList(std::unordered_map<std::string, std::unique_ptr<File>>::iterator &, const std::string &);

	static Cmd getCmd(const std::string &, uint, uint);

	const std::string getLinkPath(const std::string &);
	const std::string makeURL(const std::string &);

};

#endif