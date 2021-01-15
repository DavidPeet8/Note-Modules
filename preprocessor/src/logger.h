#ifndef LOGGER_H
#define LOGGER_H

#include "datastructs.h"
#include "io.h"


#define UNUSED(expr) do { (void)(expr); } while (0)

class Logger 
{
	static std::unique_ptr<Logger> logger;
	std::ostream &out;

public:
	enum LogLevel { NONE = 0, ERROR, WARN, INFO, DEBUG, LOG };
	LogLevel loglevel = LogLevel::NONE;

	static Logger &create();
	static Logger &create(std::ostream &out);
	static Logger &dbg();
	static Logger &info();
	static Logger &err();
	static Logger &warn();
	// Put to ostream regardless of log level
	static Logger &log(); 

	template <typename T>
	void dump(const T &);

	~Logger() { out << std::flush; }

private:
	Logger();
	Logger(std::ostream &);

};

template<typename T>
Logger &operator<< (Logger &log, const T &content)
{
	log.dump(content);
	return log;
}

template<typename T>
void Logger::dump(const T & content)
{
	switch(loglevel)
	{
		case NONE:
			break;

		case ERROR:
		#if LOGLEVEL >= 1
			out << content;
		#endif
			break;

		case WARN:
		#if LOGLEVEL >= 2
			out << content;
		#endif
			break;

		case INFO:
		#if LOGLEVEL >= 3
			out << content;
		#endif
			break;

		case DEBUG:
		#if LOGLEVEL >= 4
			out << content;
		#endif
			break;

		case LOG:
			out << content;
			break;

		default:
			UNUSED(out);
	}
}

#endif