#ifndef DFA_H
#define DFA_H

#include "datastructs.h"
#include "other.h"


class DFA 
{
	using ActionType = std::optional<std::function<void(const std::string &, unsigned &, unsigned &)>>;

public:
	enum CharType { WHITESPACE = 0, QUOTE, OTHER };
	enum DFAState { START = 0, QUOTEROOT, OTHERROOT, ERROR };

	struct Transition {
		DFAState prevState;
		DFAState newState;
		ActionType action;
	};

private:
	std::unordered_map<DFAState, std::unordered_map<CharType, Transition>> transitions;
	ActionType endHandler = std::nullopt;

public:
	void registerTransition(const DFAState state, const CharType ct, const DFAState newState, ActionType);
	void registerEndHandler(const ActionType &);
	void run(const std::string &);

private:
	CharType charToCharType(const char c);
};

#endif