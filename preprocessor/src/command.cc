#include "command.h"
#include "file.h"
#include "dfa.h"
#include "logger.h"

#include <string>
#include <vector>
#include <regex>
#include <unordered_map>
#include <optional>
#include <functional>

using namespace std;
using State = DFA::DFAState;
using CType = DFA::CharType;

Cmd::Cmd(const CmdType type, const string targetsStr): type{type}
{
	using namespace std::placeholders;
	using TransitionHandler = optional<function<void(const string &, unsigned &, unsigned &)>>;

	// Register DFA transitions
	dfa.registerTransition(State::START, CType::WHITESPACE, State::START, std::nullopt);
	dfa.registerTransition(State::START, CType::QUOTE, State::QUOTEROOT, std::nullopt);
	dfa.registerTransition(State::START, CType::OTHER, State::OTHERROOT, std::nullopt);

	dfa.registerTransition(State::OTHERROOT, CType::WHITESPACE, State::START, 
		TransitionHandler(bind(&Cmd::appendArg, this, _1, _2, _3))); // Emit argument cmd
	dfa.registerTransition(State::OTHERROOT, CType::OTHER, State::OTHERROOT, std::nullopt);
	dfa.registerTransition(State::OTHERROOT, CType::QUOTE, State::ERROR, std::nullopt);

	dfa.registerTransition(State::QUOTEROOT, CType::QUOTE, State::START, 
		TransitionHandler(bind(&Cmd::appendArg, this, _1, _2, _3))); // Emit argument cmd
	dfa.registerTransition(State::QUOTEROOT, CType::WHITESPACE, State::QUOTEROOT, std::nullopt);
	dfa.registerTransition(State::QUOTEROOT, CType::OTHER, State::QUOTEROOT, std::nullopt);

	dfa.registerEndHandler(TransitionHandler(bind(&Cmd::appendArg, this, _1, _2, _3)));

	Logger::dbg() << "TARGETS STRING:" << targetsStr << "\n";
	size_t startIdx = targetsStr.find_first_of('[') + 1;
	size_t endIdx = targetsStr.find_last_of(']');

	dfa.run(targetsStr.substr(startIdx, endIdx - startIdx));
}

Cmd Cmd::getCmd(const string &cmd)
{
	string command  = "";
	bool seen = false;
	uint start = 0, end = 0;

	Logger::dbg() << "COMMAND: " << cmd << "\n";

	for (int i = 0; i < cmd.length(); ++i)
	{
		if (seen && isspace(cmd[i]))
		{
			end = i;
			command = cmd.substr(start, end - start);
			break;
		}
		else if (seen && i == cmd.length() - 1)
		{
			end = i;
			command = cmd.substr(start, end - start + 1);
			break;
		}
		else if (!seen && !isspace(cmd[i]))
		{
			seen = true;
			start = i;
		}
	}

	return Cmd(strToCmdType(command), cmd.substr(end + 1, cmd.length() - end - 1));
}

Cmd::CmdType Cmd::strToCmdType(const string &str)
{
	Logger::dbg() << "StrToCmdType: |" << str << "|" << "\n";
	if (str == "include") { return CmdType::INCLUDE; }
	else if (str == "link") { return CmdType::LINK; }
	else if (str == "nobuild") { return CmdType::NOBUILD; }
	else if (str == "image") { return CmdType::IMG; }

	return CmdType::ERR;
}

string Cmd::cmdTypeToStr(const CmdType type)
{
	switch(type)
	{
		case CmdType::INCLUDE:
			return "include";
		case CmdType::LINK:
			return "link";
		case CmdType::NOBUILD:
			return "nobuild";
		case CmdType::IMG:
			return "image";
		default:
			return "UNRECOGNIZED";
	}
}

vector<Cmd> Cmd::getCmds(const string &rawCommand)
{
	uint cmdStart = 0;
	uint cmdEnd = 0;
	uint nestLevel = 0;
	vector<Cmd> commands = {};

	for (int i = 0; i < rawCommand.length(); ++i)
	{
		if (rawCommand[i] == '[') 
		{
			if (nestLevel == 0) { cmdStart = i; }
			++nestLevel;
		}
		else if (rawCommand[i] == ']')
		{
			--nestLevel;
			if (nestLevel == 0) 
			{ 
				cmdEnd = i; 
				commands.emplace_back(getCmd(rawCommand.substr(cmdStart + 1, cmdEnd - cmdStart - 1))); // add one to start to avoid passing [
			}
		}
	}

	return commands;
}

void Cmd::apply(const CommandHandlers &handlers) const
{
	switch (getType()) 
	{
		case Cmd::CmdType::INCLUDE:
			handlers.includeHandler(getTargets());
			break;
		case Cmd::CmdType::LINK:
			handlers.linkHandler(getTargets());
			break;
		case Cmd::CmdType::NOBUILD:
			handlers.nobuildHandler(getTargets());
			break;
		case Cmd::CmdType::IMG:
			dumpTargets();
			handlers.imgHandler(getTargets());
			break;
		case Cmd::CmdType::ERR:
			handlers.errHandler(getTargets());
			break;	
	}
}

void Cmd::appendArg(const string &targetStr, unsigned &startIdx, unsigned &length)
{
	Logger::dbg() << "Cmd::appendArg(): Appending argument: " << targetStr.substr(startIdx, length) << "\n";
	targets.emplace_back(targetStr.substr(startIdx, length));
	startIdx += length;
	length = 0;
}

void Cmd::dumpTargets() const 
{
	Logger::dbg() << "Cmd::dumpTargets(): Targets (len: " << getTargets().size() << "):" << "\n";
	for (const auto &target: getTargets())
	{
		Logger::dbg() << "  |" << target << "|" << "\n";
	}
}

