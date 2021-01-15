
#include "preprocessor_utils.h"

#include <filesystem>
#include <functional>
#include <iostream>
#include <regex>
#include <string>
#include <vector>

#include "file.h"
#include "logger.h"
#include "preprocessor.h"

using namespace std;
namespace fs = std::filesystem;

namespace Preprocessor
{
const string getLinkPath(const string &target)
{
  // This is horrible I should really fix this
  return string("/#/note/build/.flat_notes/") + string(fs::path(target).filename());
}

// There is a strange edge case where "  \n" does not create a line break if we have "**boldtxt**:
// \n"
bool isBoldColonCase(const string &line)
{
  const string pattern = "**:";
  return line.length() > 3 && line.compare(line.length() - 3, 3, pattern) == 0;
}

void includeHandler(File *const curFile, ostream &curFileStream, Preprocessor *const p,
                    const vector<string> &targets)
{
  curFileStream << "\n";
  for (const auto &target : targets) {
    Logger::info() << "Recursively Building target " << target << "\n";
    p->build(target);  // Recursively build each target to include in order
    // Copy build contents into the current file inline
    p->copyBuiltFile(curFileStream, target);
  }
}

// Link has the form <!-- [link path name] -->
void linkHandler(File *const curFile, ostream &curFileStream, const vector<string> &targets)
{
  if (targets.size() == 0) return;
  if (targets.size() == 1)
    curFileStream << " [" << fs::path(targets[0]).stem() << "](" << getLinkPath(targets[0]) << ") ";
  else if (targets.size() >= 2) {
    if (targets.size() > 2) {
      Logger::warn() << "Link command arguments ignored in link of target " << targets[0] << "\n";
      return;
    }
    curFileStream << " [" << targets[1] << "](" << getLinkPath(targets[0]) << ") ";
  }
}

void nobuildHandler(File *const curFile, ostream &curFileStream, const vector<string> &targets)
{
  curFile->setNoBuild();
}

void errHandler(File *const curFile, ostream &curFileStream, const vector<string> &targets)
{
  Logger::warn() << "Command not recognized, ignoring.\n";
}

void imgHandler(File *const curFile, ostream &curFileStream, const vector<string> &targets)
{
  curFileStream << "\n<div class=\"md-img-container\">";
  for (const auto &target : targets) {
    curFileStream << "<img class=\"md-img\" src=\"" << makeURL(target) << "\"/>";
  }
  curFileStream << "</div>\n";
}

const string makeURL(const string &target)
{
  static basic_regex pattern("https?://.*?");

  const auto matchBeginItr = sregex_iterator(target.begin(), target.end(), pattern);
  const auto matchEndItr   = sregex_iterator();

  if (matchBeginItr == matchEndItr) {
    // Assume you are reffering to a local file
    return string("http://localhost:8000/image/") + target;
  } else {
    // Assume that you put in a url properly
    return target;
  }
}
}  // namespace Preprocessor
