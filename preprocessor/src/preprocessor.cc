#include "preprocessor.h"

#include <sys/stat.h>
#include <sys/types.h>

#include <cctype>
#include <filesystem>
#include <fstream>
#include <functional>
#include <iostream>
#include <regex>
#include <unordered_map>
#include <vector>

#include "command.h"
#include "file.h"
#include "logger.h"
#include "preprocessor_utils.h"

using namespace std;
namespace fs = std::filesystem;

// TODO: finish adding support for passing directories
namespace Preprocessor
{
Preprocessor::Preprocessor(ArgParse::Args &a) :
    globalArgs(a), fileList{a.getMap()}, baseNotesDir{a.getBaseNotesPath()}
{}

// API Build function
void Preprocessor::startBuild()
{
  Logger::info() << "Initiating build ...\n";

  int status = mkdir((baseNotesDir + "/build").c_str(), S_IRWXU);
  status     = mkdir((baseNotesDir + "/build/.flat_notes").c_str(), S_IRWXU);

  File *file = fileList.begin()->second.get();

  // Loop over not visited notes
  while (!file->isVisited()) {
    Logger::info() << "Starting build for " << file->getName() << "\n";
    build(file->getName());
    file = file->getNext();
  }

  Logger::info() << "Build completed, Initiating linking step\n";
  linkBuiltFiles(fs::absolute(baseNotesDir + "/build"),
                 "");  // Must pass absolute path
}

// Add to the list of files that we will preprocess
void Preprocessor::addToFilesList(unordered_map<string, unique_ptr<File>>::iterator &itr,
                                  const string &noteName)
{
  File *prevFile = fileList.begin()->second.get();
  File *nextFile = prevFile->getNext();

  // Not in the file list but on the file system
  itr = fileList.emplace(noteName, make_unique<File>(noteName)).first;

  itr->second->setPrev(prevFile);        // Set current to point to previous node
  itr->second->setNext(nextFile);        // Set current to point to next node
  prevFile->setNext(itr->second.get());  // Set previous to point to new node
  nextFile->setPrev(itr->second.get());  // Set next to point back to current node
}

// NoBuild simply means do not make any copies out of flat notes in builddir
void Preprocessor::build(const string &noteName)
{
  using namespace std::placeholders;

  auto itr = fileList.find(noteName);
  if (itr == fileList.end() && fs::exists(baseNotesDir + "/.flat_notes/" + noteName)) {
    // File exists, but is not yet in the fileList
    addToFilesList(itr, noteName);
  } else if (itr == fileList.end()) {
    // File does not exist
    Logger::err() << "Note with name " << noteName
                  << " does not exist in .flat_notes and cannot be built\n";
    return;
  }

  File *note = itr->second.get();
  if (shouldShortCircuit(note)) {
    Logger::info() << "File is cached and already built, skipping.\n";
    return;
  }
  Logger::info() << noteName << " is not cached, building now\n";

  static basic_regex pattern("<!--.*?-->");

  note->visit();  // Visit the node and remove it from the linked list of
                  // unvisited files
  ifstream in(baseNotesDir + "/.flat_notes/" + note->getName());

  // Select an ostream - Allow for all output to one file
  ofstream fout(baseNotesDir + "/build/.flat_notes/" + note->getName());
  ostream &out = globalArgs.hasOut() ? cout : fout;

  string line = "";

  // std::bind(&Preprocessor::includeHandler, this, note, ref(out), _1), - class
  // member example
  Cmd::CommandHandlers handlers = {
      bind(includeHandler, note, ref(out), this, _1), bind(linkHandler, note, ref(out), _1),
      bind(nobuildHandler, note, ref(out), _1), bind(imgHandler, note, ref(out), _1),
      bind(errHandler, note, ref(out), _1)};

  while (getline(in, line)) {
    const char *end = isBoldColonCase(line) ? "\n\n" : "  \n";
    smatch match;

    while (regex_search(line, match, pattern)) {
      int posn = match.position();
      out << line.substr(0, posn);

      string matchedStr = match.str();
      Logger::dbg() << "Matched String: " << matchedStr << "\n";
      vector<Cmd> cmds = Cmd::getCmds(matchedStr);

      for (const auto &cmd : cmds) {
        cmd.apply(handlers);
      }

      line = line.substr(posn + match.length());
    }
    out << line << end;
  }

  out << flush;
  cache.emplace(note);  // Add the note to the cache as it is done building
}

void Preprocessor::linkBuiltFiles(const string &baseBuildPath, const string &pathTail)
{
  // Traversal over non-hidden folders recreating folder and file structure
  const auto cwd = fs::current_path();
  fs::current_path(fs::absolute(baseBuildPath + pathTail));  // cd into build directory
  fs::directory_iterator baseDir(baseNotesDir + pathTail);

  Logger::dbg() << "Linking: " << baseNotesDir + pathTail << "\n";

  for (const auto &item : baseDir) {
    string name = item.path().filename().string();
    // cerr << "Linking " << name << endl;
    string mirrorPath = baseNotesDir + "/build" + pathTail + "/" + name;

    if (name[0] == '.' || name == "build") {
      continue;
    }
    if (item.is_directory()) {
      // Create the corresponding directory under
      if (!fs::exists(mirrorPath)) {
        Logger::info() << "Directory created: " << mirrorPath << "\n";
        fs::create_directory(mirrorPath);
      }
      linkBuiltFiles(baseBuildPath,
                     pathTail + "/" + name);  // Recursively process next dir
    } else if (item.is_regular_file()) {
      if (fs::exists(mirrorPath)) {
        fs::remove(mirrorPath);
      }

      const auto itr = fileList.find(name);

      if (fs::exists(baseNotesDir + "/build/.flat_notes/" + name) && itr != fileList.end()
          && itr->second->shouldBuild())
      {
        fs::create_hard_link(baseNotesDir + "/build/.flat_notes/" + name, mirrorPath);
      }
    }
  }

  fs::current_path(cwd);
}

void Preprocessor::copyBuiltFile(ostream &curFileStream, const string &srcName)
{
  // append the contents of the built note with name noteToAppend to the
  // currentFileStream
  ifstream source(baseNotesDir + "/build/.flat_notes/" + srcName);
  curFileStream << source.rdbuf();  // send the entire contents of source
}

bool Preprocessor::shouldShortCircuit(File *note)
{
  bool isCached = cache.find(note) != cache.end();

  if (isCached) {
    return true;
  } else if (note->isVisited()) {
    Logger::err() << "Cyclic dependancy detected. Exiting.\n";
    return true;
  }
  return false;
}

}  // namespace Preprocessor
