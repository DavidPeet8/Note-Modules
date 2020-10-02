#ifndef PREPROCESSOR_H
#define PREPROCESSOR_H

#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <memory>
#include <iostream>

class File;
class Cmd;

class Preprocessor 
{
	// Store a list of files to preprocess
	std::unordered_map<std::string, std::unique_ptr<File>> &fileList;
	const std::string baseNotesDir;

	// Store a cache of files that already have been processed - indicate 
	std::unordered_set<File*> cache;

public:
	// Force the argument to be moved in 
	Preprocessor(std::unordered_map<std::string, std::unique_ptr<File>> &filesToProcess, const std::string baseNotesDir);
	
	// Build the next nonvisited file in the file list
	void build ();

private:
	// Build designated file recursively
	void build (const std::string &noteName);

	void linkBuiltFiles(const std::string &basePath, const std::string &pathTail = "");

	void copyBuiltFile(std::ostream &curFileStream, const std::string &noteToAppend);
	
	bool shouldShortCircuit(File *note);

	bool isBoldColonCase(const std::string &line);

	void addToFilesList(std::unordered_map<std::string, std::unique_ptr<File>>::iterator &, const std::string &);

	const std::string getLinkPath(const std::string &);	

	void includeHandler(File * const curFile, std::ostream &curFileStream, const std::vector<std::string> &targets);
	void linkHandler(File * const curFile, std::ostream &curFileStream, const std::vector<std::string> &targets);
	void nobuildHandler(File * const curFile, std::ostream &curFileStream, const std::vector<std::string> &targets);
	void imgHandler(File * const curFile, std::ostream &curFileStream, const std::vector<std::string> &targets);
	void errHandler(File * const curFile, std::ostream &curFileStream, const std::vector<std::string> &targets);

	const std::string makeURL(const std::string &);

};

#endif