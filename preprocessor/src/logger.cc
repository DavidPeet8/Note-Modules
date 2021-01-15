#include "logger.h"

#include <iostream>
#include <memory>
#include <string>

using namespace std;

std::unique_ptr<Logger> Logger::logger = nullptr;

Logger &Logger::create()
{
  logger.reset(new Logger());
  return *logger;
}

Logger &Logger::create(ostream &out)
{
  logger.reset(new Logger(out));
  return *logger;
}

Logger::Logger() : out{std::cerr} {}

Logger::Logger(ostream &out) : out{out} {}

Logger &Logger::dbg()
{
  logger->loglevel = LogLevel::DEBUG;
  *logger << "[ \x1b[93mDEBUG\x1b[0m ]: ";
  return *logger;
}

Logger &Logger::info()
{
  logger->loglevel = LogLevel::INFO;
  *logger << "[ \x1b[96mINFO\x1b[0m ]: ";
  return *logger;
}

Logger &Logger::warn()
{
  logger->loglevel = LogLevel::WARN;
  *logger << "[ \x1b[95mWARN\x1b[0m ]: ";
  return *logger;
}

Logger &Logger::err()
{
  logger->loglevel = LogLevel::ERROR;
  *logger << "[ \x1b[91mERROR\x1b[0m ]: ";
  return *logger;
}

Logger &Logger::log()
{
  logger->loglevel = Logger::LOG;
  return *logger;
}
