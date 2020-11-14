#include "args.h"

#include <cassert>
#include <cmath>
#include <filesystem>
#include <iostream>
#include <memory>
#include <optional>
#include <string>

#include "file.h"
#include "logger.h"

using namespace std;
namespace fs  = std::filesystem;
using FileMap = unordered_map<string, unique_ptr<File>>;
using FlagMap = unordered_map<ArgParse::FlagType, vector<string>>;

namespace
{
void addFileToFileList(FileMap &filesToProcess, const fs::path &filepath)
{
  Logger::dbg() << "Adding File " << filepath.filename() << " to file map\n";

  if (filesToProcess.find(filepath.filename()) != filesToProcess.end()) {
    // File already exists in the map so we do nothing
    return;
  }

  unique_ptr<File> f = make_unique<File>(filepath.filename());

  // Use the idea of inserting into a circle will preserve traversablility
  if (filesToProcess.empty()) {
    f->setNext(f.get());
    f->setPrev(f.get());
  } else {
    File *first  = filesToProcess.begin()->second.get();
    File *second = first->getNext();

    first->setNext(f.get());
    second->setPrev(f.get());
    f->setPrev(first);
    f->setNext(second);
  }

  filesToProcess[filepath.filename()] = move(f);
}

void addDirToFileList(FileMap &filesToProcess, const fs::path &dirpath)
{
  // Iterate over the directory path given, recursively add all files to the file list
  fs::recursive_directory_iterator dirit(dirpath);  // Set up the dir iterator

  for (const auto &entry : dirit) {
    if (!entry.is_directory()) {
      // It is some file we can add
      addFileToFileList(filesToProcess, entry.path());
    }
    // No need for an else case, this is a recursive iterator
  }
}

void addToFileList(FileMap &filesToProcess, const fs::path &path)
{
  if (fs::is_directory(path)) {
    addDirToFileList(filesToProcess, path);
  } else {
    addFileToFileList(filesToProcess, path);
  }
}
}  // namespace

namespace ArgParse
{
Args::Args(const FlagMap &flags, const vector<string> &positionalArgs) :
    baseNotesPath(), filesToProcess()
{
  int startIdx = 0;  // Index to start reading the file list from in positonal args

  initFlags(flags);

  if (baseNotesPath == "") {
    // BaseNotes Path was not set by the --path argument, assume it is first positional arg
    baseNotesPath = fs::absolute(positionalArgs[0]).string();
    startIdx      = 1;
  }

  if (positionalArgs.size() == 0) {
    Logger::err() << "Insufficent number of arguments supplied.\n";
    exit(1);
  } else if (positionalArgs.size() == 1) {
    initNoFileList();
  } else {
    initFileList(positionalArgs, startIdx);
  }
}

void Args::initFileList(const vector<string> &positionalArgs, int startIdx)
{
  Logger::info() << "Initializing from provided file list\n";

  unsigned numArgs = positionalArgs.size();

  // Set hashtable size to be argc^2 to attempt to minimize probability of collision
  // Assuming we have no directories listed
  filesToProcess.reserve(pow(numArgs, 2));

  for (unsigned i = startIdx; i < numArgs; i++) {
    addToFileList(filesToProcess, fs::path(positionalArgs[i]));
  }
}

void Args::initFlags(const FlagMap &flags)
{
  FlagMap::const_iterator it;

  if ((it = flags.find(FlagType::OSTREAM)) != flags.end()) {
    outputToConsole = true;
  }
  if ((it = flags.find(FlagType::BASE_PATH)) != flags.end()) {
    baseNotesPath = fs::path(it->second[0]).string();
  }
}

void Args::initNoFileList()
{
  Logger::warn() << "No files specified defaulting to initializing from no file list\n";

  fs::directory_iterator dirit(baseNotesPath + "/.flat_notes");
  fs::recursive_directory_iterator rit(baseNotesPath + "/.flat_notes");

  for (const auto &entry : rit) {
    addToFileList(filesToProcess, entry.path());
  }
}

void Args::dump() const
{
  Logger::log() << "\n"
                << "----------------- FILES TO PROCESS ---------------- \n";
  for (const auto &entry : filesToProcess) {
    Logger::log() << entry.first << "\n";
    Logger::log() << "FileList entry ptr:" << entry.second.get() << "\n";
    Logger::log() << "\tnext ptr:" << entry.second->getNext() << "\n";
    Logger::log() << "\tprev ptr:" << entry.second->getPrev() << "\n";
  }
}

}  // namespace ArgParse
