#ifndef ARGS_H
#define ARGS_H

#include "arg_utils.h"
#include "file.h"
#include <vector>
#include <string>
#include <list>
#include <unordered_map>
#include <memory>
#include <optional>

class File;

namespace ArgParse
{

	class Args
	{
		std::string baseNotesPath = "";
		std::unordered_map<std::string, std::unique_ptr<File>> filesToProcess;
		bool outputToConsole = false;

	public:
		Args(const std::unordered_map<FlagType, std::optional<std::string>> &flags, 
			 const std::vector<std::string> &positionalArgs);

		void dump() const;
		std::unordered_map<std::string, std::unique_ptr<File>> &getMap() { return filesToProcess; }
		std::string getBaseNotesPath() const { return baseNotesPath; }
		bool hasOut() const { return outputToConsole; }

	private:
		void initFileList(const std::vector<std::string> &positionalArgs, int startIdx);
		void initNoFileList();
		void initFlags(const std::unordered_map<FlagType, std::optional<std::string>> &flags);
	};

}

#endif