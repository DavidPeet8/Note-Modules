#include "file.h"
#include "args.h"
#include "arg_parser.h"
#include "preprocessor.h"
#include "logger.h"

#include <iostream>

using namespace std;

/*
The following directives are to be recognized

[//]: # (nobuild) -- To avoid appearing in filters after build
[//]: # (import [name of note to copy paste in])

*/
// argv[0] = proc name
// argv[1] = path to .flat_notes
// argv[i>1] = file name to build
int main(int argc, char **argv) 
{
	ios_base::sync_with_stdio(false);
	cin.tie(nullptr);

	Logger::create(std::cerr);

	if (argc < 2) 
	{
		Logger::err() << "Not Enough arguments\n";
		return 0;
	}
	
	ArgParse::ArgParser parser;
	ArgParse::Args a = parser.parse(argc, argv);
	// a.dump();
	
	Preprocessor::Preprocessor preproc(a);
	preproc.startBuild();
}