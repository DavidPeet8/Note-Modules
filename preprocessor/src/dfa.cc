#include "dfa.h"
#include "logger.h"
#include <string>
#include <vector>
#include <functional>
#include <cctype>

using namespace std;
using State = DFA::DFAState;
using CType = DFA::CharType;
using ActionType = std::optional<std::function<void(const std::string &, unsigned &, unsigned &)>>;

void DFA::registerTransition(const DFAState state, const CharType ct, const DFAState newState, ActionType action)
{
	transitions[state][ct] = Transition {state, newState, action};
}

void DFA::registerEndHandler(const ActionType &action)
{
	if (action.has_value())
	{
		endHandler = action;
	}
}

void DFA::run(const string &targetsStr) 
{
	State curState = State::START;
	unsigned startIdx = 0;
	unsigned length = 0;

	Logger::dbg() << "DFA::run() recieved target string: " << targetsStr << "\n";
	for (const auto &c : targetsStr) 
	{
		length++;
		CType character = charToCharType(c);
		Transition &trans = transitions[curState][character];
		curState = trans.newState;

		if (curState == State::ERROR) 
		{ 
			Logger::err() << "Hit error state when parsing.\n";
			throw "Oops hit error state when parsing."; 
		}

		// If the transition has a valid action, perform it
		if (trans.action.has_value())
		{
			// Pass in the current string
			trans.action.value()(targetsStr, startIdx, length); 
		}
	}

	if (endHandler.has_value())
	{
		endHandler.value()(targetsStr, startIdx, length);
	}
}	

CType DFA::charToCharType(const char c)
{
	if (c == '"') { return CType::QUOTE; }
	else if (isspace(c)) { return CType::WHITESPACE; }
	else { return CType::OTHER;	}
}