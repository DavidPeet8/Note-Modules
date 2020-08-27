#ifndef FILE_H
#define FILE_H

#include <string>

class File
{
	const std::string name;
	bool visited = false;
	bool willBuild = true;

	// Non-owning pointers to the next/prev non visited node
	File *next;
	File *prev;

public:
	File(const std::string &name): name(name){}

	void visit() 
	{ 
		visited = true; 
		prev->setNext(next); // Non owning no delete needed
	}
	bool isVisited() const { return visited; }
	void setPrev(File * file) { prev = file; }
	void setNext(File * file) { next = file; }
	File *getNext() const { return next; }
	File *getPrev() const { return prev; }
	void setNoBuild(){ willBuild = false; }
	const std::string &getName() const { return name; }
};

#endif
