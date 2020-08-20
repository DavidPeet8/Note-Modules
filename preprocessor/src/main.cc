#include "file.h"
#include "args.h"
#include "preprocessor.h"

#include <iostream>
#include <bits/stdc++.h>

using namespace std;

/*
The following directives are to be recognized

[//]: # (build=[true/false])                                 | Default to true if not stated
[//]: # (import [name of note to copy paste in])

*/
// argv[0] = proc name
// argv[1] = path to .flat_notes
// argv[i>1] = file name to build
int main(int argc, char **argv) 
{
	ios_base::sync_with_stdio(false);
	cin.tie(nullptr);
	
	Args a(argc, argv);

	auto &fileList = a.getMap();
}