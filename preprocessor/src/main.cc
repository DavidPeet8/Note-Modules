#include <iostream>

#include "arg_parser.h"
#include "args.h"
#include "file.h"
#include "logger.h"
#include "preprocessor.h"

using namespace std;

/*
The following directives are to be recognized

[//]: # (nobuild) -- To avoid appearing in filters after build
[//]: # (import [name of note to copy paste in])

*/
// argv[0] = proc name
// argv[1] = path to .notes
// argv[i>1] = file name to build

// TODO: allow directory paths as well as file names
// Maybe prefix each directory with -d or --dir
int main(int argc, char **argv)
{
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);

  Logger::create(std::cerr);

  if (argc < 2) {
    Logger::err() << "Not Enough arguments\n";
    return 0;
  }

  ArgParse::ArgParser parser;
  ArgParse::Args a = parser.parse(argc, argv);

  Preprocessor::Preprocessor preproc(a);
  preproc.startBuild();
}
