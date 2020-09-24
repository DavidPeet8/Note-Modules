# include <iostream>
# include <regex>
# include <filesystem>
# include <utility>
# include <fstream>
# include <unordered_map>
# include <algorithm>

using namespace std;
namespace fs = std::filesystem;

void search(const string & basePath, const string &pattern, const bool deep_search, unordered_map<string, uint> &results)
{
	static basic_regex patt(pattern);

	for(auto &item : fs::directory_iterator(basePath))
	{
		string fileName = item.path().filename();
		if (item.is_directory())
		{
			search(item.path(), pattern, deep_search, results);
		} 
		else if (sregex_iterator(fileName.begin(), fileName.end(), patt) != sregex_iterator())
		{
			results[fileName] = 1; // can assume it didn't exist before as all files are unique
		}

		// Check if deep search is requested
		if (deep_search)
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
					++results[fileName];
				}
				else 
				{
					results[fileName] = 1;
				}
			}
		}
	}
}

void print_results(const unordered_map<string, uint> &results)
{
	cerr << "Printing Results" << endl;
	for (const auto &p: results)
	{
		cout << p.first << " | " << p.second << "\n";
	}
	cout << flush;
}

// This is a search engine for searching
int main(int argc, char **argv)
{
	ios_base::sync_with_stdio(false);
	cin.tie(nullptr);

	if (argc != 4) { return 1; }
	const string basePath = argv[1];
	const string pattern = argv[2];
	const bool deep_search = argv[3];

	unordered_map<string, uint> results {};
	search(basePath, pattern, deep_search, results);

	print_results(results);
	
}




