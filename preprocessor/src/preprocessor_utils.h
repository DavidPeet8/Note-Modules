# ifndef PREPROCESSOR_UTILS_H
# define PREPROCESSOR_UTILS_H

#include "datastructs.h"
#include "io.h"


class File;

namespace Preprocessor
{
	class Preprocessor;

	const std::string getLinkPath(const std::string &);	

	void includeHandler(File * const curFile, 
						std::ostream &curFileStream,
						 Preprocessor * const p,
						const std::vector<std::string> &targets);
	void linkHandler(File * const curFile, std::ostream &curFileStream, const std::vector<std::string> &targets);
	void nobuildHandler(File * const curFile, std::ostream &curFileStream, const std::vector<std::string> &targets);
	void imgHandler(File * const curFile, std::ostream &curFileStream, const std::vector<std::string> &targets);
	void errHandler(File * const curFile, std::ostream &curFileStream, const std::vector<std::string> &targets);

	const std::string makeURL(const std::string &);

	bool isBoldColonCase(const std::string &line);
}

#endif 
