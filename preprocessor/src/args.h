#ifndef ARGS_H
#define ARGS_H

#include <vector>
#include <string>
#include <list>
#include <unordered_map>
#include <memory>

class File;

struct Args
{
	std::string baseNotesPath;
	std::unordered_map<std::string, std::unique_ptr<File>> filesToProcess;

public:
	Args(int argc, const char * const * const argv);
	void printDirList();
	std::unordered_map<std::string, std::unique_ptr<File>> &getMap() { return filesToProcess; }
	std::string getBaseNotesPath() { return baseNotesPath; }

private:
	void initFileList(int argc, const char * const * const argv);
	void initNoFileList();
};

#endif