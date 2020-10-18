#ifndef PREPROCESSOR_H
#define PREPROCESSOR_H

#include "args.h"

#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <memory>
#include <iostream>

class File;
class Cmd;

namespace Preprocessor
{

	class Preprocessor 
	{
		// Store a list of files to preprocess
		ArgParse::Args &globalArgs;
		std::unordered_map<std::string, std::unique_ptr<File>> &fileList;
		const std::string baseNotesDir;

		// Store a cache of files that already have been processed - indicate 
		std::unordered_set<File*> cache;

		friend void includeHandler(File * const, std::ostream &, Preprocessor * const p, const std::vector<std::string> &);

	public:
		// Force the argument to be moved in 
		Preprocessor(ArgParse::Args &a);
		
		// Build the next nonvisited file in the file list
		void startBuild ();

	private:
		// Build designated file recursively
		void build (const std::string &noteName);

		void linkBuiltFiles(const std::string &basePath, const std::string &pathTail = "");

		void copyBuiltFile(std::ostream &curFileStream, const std::string &noteToAppend);
		
		void addToFilesList(std::unordered_map<std::string, std::unique_ptr<File>>::iterator &, const std::string &);
		bool shouldShortCircuit(File *note);
	};

}

#endif