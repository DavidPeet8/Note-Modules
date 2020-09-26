# include <iostream>
# include <regex>
# include <filesystem>
# include <utility>
# include <fstream>
# include <unordered_map>
# include <algorithm>

using namespace std;
namespace fs = std::filesystem;

void search(const string & basePath, const string &pattern, const bool deep, unordered_map<string, uint> &results)
{
	static basic_regex patt(pattern);

	for(auto &item : fs::directory_iterator(basePath))
	{
		string fileName = item.path().filename();
		if (item.is_directory())
		{
			search(item.path(), pattern, deep, results);
		} 
		else if (sregex_iterator(fileName.begin(), fileName.end(), patt) != sregex_iterator())
		{
			results[fileName] = 1; // can assume it didn't exist before as all files are unique
		}

		// Check if deep search is requested
		if (deep)
		{
			fstream file {item.path()};
			string line = "";

			// Go line by line through the file getting matches
			while (getline(file, line)) 
			{
				uint occur = 0;
				for (auto it = sregex_iterator(line.begin(), line.end(), patt); it != sregex_iterator(); ++it)
				{
					++occur;
				}

				if (occur < 1) { continue; }
				else if (results.find(fileName) != results.end())
				{
					results[fileName] += occur;
				}
				else 
				{
					results[fileName] = 1;
				}
			}
		}
	}
}

struct Args 
{
	bool deep = false;
	bool json = false;
	string pattern = "";
	vector<string> targets = {};

	void dump()
	{
		cerr << "--------- Args ---------\n";
		cerr << "Deep Search: " << deep << "\n";
		cerr << "Pattern: " << pattern << "\n";
		cerr << "Targets: \n";

		for (const auto &target : targets)
		{
			cerr << target << "\n";
		}
		cerr << flush;
	}
};

// Could be faster by using a DFA, but small number of options makes this essentially constant time regardless
Args parse_args(int argc, char **argv)
{
	if (argc < 3) { exit(1); }
	
	Args a;

	for (int idx = 1; idx < argc; idx++)
	{
		if (strcmp(argv[idx], "-d") == 0 || strcmp(argv[idx], "--deep") == 0) { a.deep = true; }
		else if (strcmp(argv[idx], "-j") == 0 || strcmp(argv[idx], "--json") == 0) { a.json = true; }
		else if (a.pattern == "") 
		{ 
			a.pattern = argv[idx];
		}
		else
		{
			a.targets.emplace_back(argv[idx]);
		}
	}
	return a;
}

void print_results(const unordered_map<string, uint> &results, const bool json)
{
	cerr << "Printing Results" << endl;
	cout << (json ? "[\n" : "");
	for (const auto &p: results)
	{
		cout << (json ? "[" : "") << p.first << " " << p.second << (json ? "]" : "") << "\n";
	}
	cout << (json ? "]\n" : "") << flush;
}

// This is a search engine for searching
int main(int argc, char **argv)
{
	ios_base::sync_with_stdio(false);
	cin.tie(nullptr);

	Args args = parse_args(argc, argv);
	args.dump();
	
	unordered_map<string, uint> results {};
	for (const auto &path : args.targets)
	{
		search(path, args.pattern, args.deep, results);
	}
	
	print_results(results, args.json);
}




