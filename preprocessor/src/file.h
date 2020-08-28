#ifndef FILE_H
#define FILE_H

#include <string>
#include <iostream>

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
		prev->setNext(next); // Non owning no delete needed
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
