#ifndef FILE_H
#define FILE_H

#include <string>

class File
{
	const std::string name;
	bool visited = false;

	// Non-owning pointers to the next/prev non visited node
	File *next;
	File *prev;

public:
	File(const std::string &name): name(name){}

	void cp(const std::string &targetDirPath);
	void visit() { visited = true; }
	void setPrev(File * file) { prev = file; }
	void setNext(File * file) { next = file; }
};

#endif
