#include "args.h"
#include "file.h"

#include <string>
#include <cmath>
#include <experimental/filesystem>
#include <iostream>
#include <memory>

using namespace std;
namespace fs = std::experimental::filesystem;

Args::Args(int argc, const char * const * const argv): flatNotesPath(argv[1]), filesToProcess()
{
	if (argc > 2) // All files in flat_notes should be added to the list of files to process
	{
		initFileList(argc, argv);
	}
	else if (argc == 2)
	{
		initNoFileList();
	}
	else 
	{
		cerr << "Not enough arguments supplied." << endl;
		throw ":(";
	}
	
}

void Args::initFileList(int argc, const char * const * const argv)
{
	// Set hashtable size to be argc^2 to attempt to minimize probability of collision
	filesToProcess.reserve(pow(argc, 2));

	cerr << "Initializing from provided file list" << endl;

	for (int i = 2; i < argc; ++i)
	{
		std::unique_ptr<File> f = make_unique<File>(argv[i]);
		if (i > 2)
		{
			f->setPrev(filesToProcess[argv[i-1]].get());
			filesToProcess[argv[i-1]]->setNext(f.get());
		}	
		filesToProcess[argv[i]] = move(f);
	}

	// All linked up but last node does not have a next, and first does not have a prev
	filesToProcess[argv[2]]->setPrev(filesToProcess[argv[argc - 1]].get());
	filesToProcess[argv[argc - 1]]->setNext(filesToProcess[argv[2]].get());
}

void Args::initNoFileList()
{
	fs::directory_iterator dirit(flatNotesPath);
	File * prev = nullptr; // Non-owning ref
	File * first = nullptr;

	cerr << "Initializing from no file list" << endl; 

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

void Args::printDirList() 
{
	for (const auto &entry : filesToProcess)
	{
		cout << entry.first << endl;
	}
}