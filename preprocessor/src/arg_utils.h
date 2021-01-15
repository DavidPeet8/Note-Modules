#ifndef ARG_UTILS_H
#define ARG_UTILS_H

#include <string>

#include "datastructs.h"

namespace ArgParse
{
// -c | --console | -u / --dump-args | -p <arg> / --path <arg>
enum class FlagType
{
  OSTREAM,
  DUMP_ARGS,
  BASE_PATH,
  UNRECOGNIZED
};

std::string flagTypeToStr(const FlagType type);

FlagType getFlagType(const std::string &flag);

// Return if a flag has an argument
bool hasArgument(const FlagType);

bool isFlag(const std::string &arg);
bool isPositional(const std::string &arg);
}  // namespace ArgParse

#endif
