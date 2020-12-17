#include <iostream>

#include "arg_parser.h"
#include "args.h"
#include "file.h"
#include "logger.h"
#include "preprocessor.h"

using namespace std;

void printInvocation(int argc, char **argv)
{
  for (int i = 0; i < argc; i++) {
    Logger::log() << argv[i] << "\n";
  }
}

/*
The following directives are to be recognized

[//]: # (nobuild) -- To avoid appearing in filters after build
[//]: # (import [name of note to copy paste in])

*/
// argv[0] = proc name
// argv[1] = path to .notes
// argv[i>1] = file name to build
int main(int argc, char **argv)
{
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);

  // printInvocation(argc, argv);

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
