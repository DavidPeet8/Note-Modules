#ifndef FILE_H
#define FILE_H

#include "datastructs.h"

class File
{
	const std::string name;

	File *next, *prev;
	bool visited, willBuild;

public:
	File(const std::string &name): 
	name(name), 
	next{nullptr},
	prev{nullptr},
	visited{false}, 
	willBuild{true} {}

	void visit() 
	{ 
		visited = true; 
		// Non owning no delete needed
		prev->setNext(next); 
		next->setPrev(prev); 
	}
	bool isVisited() const { return visited; }
	void setPrev(File * file) {	prev = file; }
	void setNext(File * file) { next = file; }
	File *getNext() const { return next; }
	File *getPrev() const { return prev; }
	void setNoBuild(){ willBuild = false; }
	bool shouldBuild() const { return willBuild; }
	const std::string &getName() const { return name; }
};

#endif
