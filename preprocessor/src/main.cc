#include "file.h"
#include "args.h"
#include "preprocessor.h"

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

	if (argc < 2) 
	{
		cerr << "Not Enough arguments" << endl;
		return 0;
	}
	
	Args a(argc, argv);
	auto &fileList = a.getMap(); // List of files to preprocess	
	// a.printDirList();

	Preprocessor preproc(fileList, a.getBaseNotesPath());
	preproc.build();
}