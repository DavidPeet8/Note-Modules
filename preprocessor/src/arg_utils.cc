#include "arg_utils.h"

#include <string>

#include "logger.h"

namespace ArgParse
{
std::string flagTypeToStr(const FlagType type)
{
  switch (type) {
    case FlagType::OSTREAM:
      return "ostream (-c | --console): ";
    case FlagType::DUMP_ARGS:
      return "dump_args (-u | --dump-args): true";
    case FlagType::BASE_PATH:
      return "path to flat notes (-p | --path): ";
    case FlagType::UNRECOGNIZED:
      return "UNRECOGNIZED FLAG";
  }
}

bool isPositional(const std::string &arg)
{
  return !isFlag(arg);
}

bool hasArgument(const FlagType type)
{
  switch (type) {
    case FlagType::OSTREAM:
      return false;
    case FlagType::DUMP_ARGS:
      return false;
    case FlagType::BASE_PATH:
      return true;
    case FlagType::UNRECOGNIZED:
      return false;
  }
}

bool isFlag(const std::string &arg)
{
  if (arg.length() == 0) {
    Logger::err() << "Somehow we got an argument of length 0 ... This should be impossible\n";
    return false;
  }

  if (arg[0] == '-') {
    return true;
  }
  return false;
}

FlagType getFlagType(const std::string &flag)
{
  if (flag == "-c" || flag == "--console") {
    return FlagType::OSTREAM;
  } else if (flag == "-u" || flag == "--dump-args") {
    return FlagType::DUMP_ARGS;
  } else if (flag == "-p" || flag == "--path") {
    return FlagType::BASE_PATH;
  }

  return FlagType::UNRECOGNIZED;
}
}  // namespace ArgParse
