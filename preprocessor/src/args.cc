#include "args.h"
#include "file.h"
#include "logger.h"

#include <string>
#include <cmath>
#include <filesystem>
#include <iostream>
#include <memory>
#include <optional>
#include <cassert>

using namespace std;
namespace fs = std::filesystem;
namespace ArgParse
{

	Args::Args(const unordered_map<FlagType, optional<string>> &flags, 
			   const vector<string> &positionalArgs):
	baseNotesPath(),
	filesToProcess()
	{
		int startIdx = 0; // Index to start reading the file list from in positonal args

		initFlags(flags);

		if (baseNotesPath == "")
		{
			// BaseNotes Path was not set by the --path argument, assume it is first positional arg
			baseNotesPath = fs::absolute(positionalArgs[0]).string();
			startIdx = 1;
		}

		if (positionalArgs.size() == 0)
		{
			Logger::err() << "Insufficent number of arguments supplied.\n";
			exit(1);
		}
		else if (positionalArgs.size() == 1)
		{
			initNoFileList();
		}
		else 
		{
			initFileList(positionalArgs, startIdx);
		}
	}

	void Args::initFileList(const vector<string> &positionalArgs, int startIdx)
	{
		Logger::info() << "Initializing from provided file list\n";
		
		unsigned numArgs = positionalArgs.size();

		// Set hashtable size to be argc^2 to attempt to minimize probability of collision
		filesToProcess.reserve(pow(numArgs, 2));
		bool fistIteration = true;

		for (unsigned i = startIdx; i < numArgs; i++)
		{
			auto entry = fs::path(positionalArgs[i]).filename();
			std::unique_ptr<File> f = make_unique<File>(entry);

			if (!fistIteration)
			{
				auto prev = fs::path(positionalArgs[i-1]).filename();
				f->setPrev(filesToProcess[prev].get());
				filesToProcess[prev]->setNext(f.get());
			}

			filesToProcess[entry] = move(f);
			fistIteration = false;
		}

		// All linked up but last node does not have a next, and first does not have a prev
		filesToProcess[fs::path(positionalArgs[1]).filename()]->setPrev(filesToProcess[fs::path(positionalArgs[numArgs - 1]).filename()].get());
		filesToProcess[fs::path(positionalArgs[numArgs - 1]).filename()]->setNext(filesToProcess[fs::path(positionalArgs[1]).filename()].get());

		assert(positionalArgs.size() == filesToProcess.size() || positionalArgs.size() - 1 == filesToProcess.size());
	}

	void Args::initFlags(const unordered_map<FlagType, optional<string>> &flags)
	{
		unordered_map<FlagType, optional<string>>::const_iterator it;
		
		if ((it = flags.find(FlagType::OSTREAM)) != flags.end())
		{
			outputToConsole = true;
		}
		if ((it = flags.find(FlagType::BASE_PATH)) != flags.end())
		{
			baseNotesPath = fs::path(it->second.value()).string();
		}
	}

	void Args::initNoFileList()
	{
		Logger::warn() << "No files specified defaulting to initializing from no file list\n"; 

		fs::directory_iterator dirit(baseNotesPath + "/.flat_notes");
		File * prev = nullptr; // Non-owning ref
		File * first = nullptr;

		for (const auto & entry : dirit)
		{
			std::string filename = entry.path().filename();
			std::unique_ptr<File> f = make_unique<File>(filename);

			if (prev != nullptr) 
			{
				prev->setNext(f.get());
				f->setPrev(prev);
			}
			if (first == nullptr) { first = f.get(); }
			prev = f.get();
			filesToProcess[filename] = move(f);
		}
		// All linked up but last node does not have a next and first does not have a prev
		first->setPrev(prev);
		prev->setNext(first);
	}

	void Args::dump() const
	{
		Logger::log() << "\n" << "----------------- FILES TO PROCESS ---------------- \n";
		for (const auto &entry : filesToProcess)
		{
			Logger::log() << entry.first << "\n";
			Logger::log() << "FileList entry ptr:" << entry.second.get() << "\n";
			Logger::log() << "\tnext ptr:"<< entry.second->getNext() << "\n";
			Logger::log() << "\tprev ptr:" << entry.second->getPrev() << "\n";
		}
	}

}