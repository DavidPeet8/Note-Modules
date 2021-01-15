# ifndef ARG_PARSER_H
# define ARG_PARSER_H

#include "args.h"
#include "arg_utils.h"
#include "datastructs.h"
#include "other.h"

namespace ArgParse 
{

	class ArgParser 
	{
		std::vector<std::string> positionalArgs;
		std::unordered_map<FlagType, std::vector<std::string>> flags;

	public:
		ArgParser() = default;

		Args parse(int argc, const char * const * const argv);

	private:
		// Pretty print all arguments parsed
		void dump() const;
	};

}

# endif
