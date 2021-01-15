#ifndef COMMAND_H
#define COMMAND_H

#include "dfa.h"
#include <vector>
#include <string>
#include <functional>
#include <iostream>
#include <vector>

class File;

class Cmd 
{
public:
	enum CmdType { INCLUDE = 0, LINK, NOBUILD, IMG, ERR };

	struct CommandHandlers
	{
		const std::function<void(const std::vector<std::string> &)> &includeHandler;
		const std::function<void(const std::vector<std::string> &)> &linkHandler;
		const std::function<void(const std::vector<std::string> &)> &nobuildHandler;
		const std::function<void(const std::vector<std::string> &)> &imgHandler;
		const std::function<void(const std::vector<std::string> &)> &errHandler;
	};

private:
	const CmdType type;
	DFA dfa;
	std::vector<std::string> targets;

public:
	static std::vector<Cmd> getCmds(const std::string &rawCommand);
	static CmdType strToCmdType(const std::string &);
	static std::string cmdTypeToStr(const CmdType);

	Cmd(const CmdType type, const std::string targetsStr);

	CmdType getType() const { return type; }
	const std::vector<std::string> &getTargets() const { return targets; }
	void apply(const CommandHandlers &) const;
	void dumpTargets() const;

private:
	static Cmd getCmd(const std::string &);
	void appendArg(const std::string &, unsigned &, unsigned &);

};

#endif