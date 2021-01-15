#include "arg_parser.h"
#include "logger.h"
#include "args.h"

#include <vector>
#include <string>
#include <optional>

namespace ArgParse
{

	Args ArgParser::parse(int argc, const char * const * const argv)
	{
		// Start at 1 as arg 0 is the path calling the executable
		for (int i = 1; i < argc; i++)
		{
			std::string arg(argv[i]);
			
			if (isFlag(arg)) // Is Flag type argument
			{
				FlagType type = getFlagType(arg);

				if (type == FlagType::UNRECOGNIZED)
				{
					Logger::warn() << "Unrecognized flag " << arg << " ignoring ...\n";
					continue;
				}

				if (hasArgument(type)) // Flag has an associated argument
				{
					i += 1;
					std::string argument;
					if (i >= argc)
					{
						Logger::err() << "Missing mandatory argument for flag: " << arg << "\n";
						argument = "";
						exit(1);
					}
					else 
					{
						argument = argv[i];
					}

					flags[type].emplace_back(argument);
				}
				else 
				{
					// Still must insert the flag key into the map to register it
					flags[type] = {};
				}
			}
			else // Is a positional argument
			{
				// We have a positional Argument, just push it back keeping order
				positionalArgs.emplace_back(argv[i]);
			}
		}

		// Now proceed to creating the Arguments Object
		Args args(flags, positionalArgs);

		// Dump args if we were asked to
		if (flags.find(FlagType::DUMP_ARGS) != flags.end())
		{
			dump();
			Logger::info() << "Dumping Arguments and Exiting without preprocssing files.\n";
			args.dump();
			exit(0); // Exit the program without proceeding to preprocess anything
		}

		return args;
	}

	void ArgParser::dump() const
	{
		Logger::log() << "\n" << "------------------------ FLAGS ------------------------ \n";
		for (const auto & entry: flags)
		{
			if (entry.second.size() > 0)
			{
				Logger::log() << flagTypeToStr(entry.first) << ":";
				for (const auto &arg : entry.second)
				{
					Logger::log() << "\t" << arg << "\n"; 
				}
			}
			else 
			{
				Logger::log() << flagTypeToStr(entry.first) << "\n";
			}
		}

		Logger::log() << "\n" << "----------------- POSITIONAL ARGUMENTS ---------------- \n";
		for (const auto &entry: positionalArgs)
		{
			Logger::log() << entry << "\n";
		}
	}

}