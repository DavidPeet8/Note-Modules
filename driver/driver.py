#! /usr/bin/python3

import cmd, sys, os, shutil, re
import shlex
from fs_helpers import *
from color_scheme import print_dir, get_prompt
from process_manager import (
    reap_pid,
    open_default,
    spawn,
    spawn_quiet,
    run,
    spawn_attach_stdout,
)
from argparser import *
import readline

sys.path.insert(1, os.path.expanduser("~/.notes_cfg/exe/searchLib"))
from search import searchDirList, dumpMap

sys.path.insert(1, os.path.expanduser("~/.notes_cfg/exe/configLib"))
from config_reader import *

hasStartedFileServer = False
args = get_driver_args(sys.argv[1:])

if args.path:
    update_base_path(args.path)

if not os.path.isdir(get_notes_path()):
    os.mkdir(get_notes_path())
os.chdir(get_notes_path())  # Set working directory to base of notes directory

# This is needed to autocomplete with the + symbol
old_delims = readline.get_completer_delims()
readline.set_completer_delims(old_delims.replace("+", ""))


def invalid(reason=""):
    print("Invalid Command.")
    if reason != "":
        print(reason)


class NoteShell(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.intro = """
Welcome to NoteShell.
Author: David Peet
Github: davidpeet8
Type help or ? for a list of commands.
		"""
        self.promptBase = "(NoteShell) "
        self.promptPath = ""
        self.promptTerminator = ": "
        self.prompt = get_prompt(
            self.promptBase, self.promptPath, self.promptTerminator
        )

    # should recieve no arguments
    def do_init(self, arg):
        check_and_mkdirs([
            get_flat_notes_path(),
            get_notes_path() + "/build",
            get_notes_path() + "/.config",
            get_notes_path() + "/.assets",
        ])
        temp_chdir_run(get_notes_path(), self.do_git, ["init"])

    # Directory to open in text editor
    def do_edit(self, args):
        rawarglist = shlex.split(args)
        temp_chdir_run(get_flat_notes_path(), self.edit_files, [rawarglist])

    def do_ls(self, args):
        arglist = shlex.split(args)
        firstArg = arglist[0].lower() if arglist else ""
        isAll, arr = False, []

        args = get_ls_args(arglist)

        if args.all:
            isAll = True
            dirPath = args.path
        elif args.notes:
            dirPath = get_flat_notes_path()
        else:
            dirPath = args.path

        arr = os.scandir(dirPath)

        try:
            for entry in arr:
                if not isAll and entry.name.startswith("."):
                    continue
                if entry.is_dir():
                    print_dir(entry.name)
                else:
                    print(entry.name)
        except:
            invalid()

    def do_cat(self, arg):
        text = self.cat_helper(arg)
        if text != "":
            print(text)

    def do_cd(self, arg):
        try:
            if arg.startswith("/"):
                os.chdir(get_notes_path()) # Change back to root dir
                if arg != "/":
                    os.chdir(arg[1:])
            else:
                os.chdir(arg);
            promptPath = os.getcwd().split(os.path.basename(get_notes_path()), 1)
            self.promptPath = (
                promptPath[1]
                if isinstance(promptPath, list) and len(promptPath) > 1
                else "/"
            )
        except:
            invalid(
                "Check that the filter exists, and that you have execute permission"
            )

    def do_create(self, args):
        arglist = shlex.split(args)

        args = get_create_args(arglist)
        if not args.filter and not args.note:
            invalid("Must specify -f or -n")
            return
        elif (args.filter and len(args.filter) < 1) or (
            args.note and len(args.note) < 1
        ):
            invalid("Both -f and -n require an argument")

        if args.filter:
            for f in args.filter:
                check_and_mkdir(f)

        if args.note:
            for n in args.note:
                if os.path.exists(get_flat_notes_path() + "/" + n):
                    print("A note of this name already exists in .flat_notes")
                    print(
                        "To add this note to the specified directory use the add command"
                    )
                    print(
                        "To remove this file permanantly use the remove command with the -p flag"
                    )
                    continue
                touch_file(get_flat_notes_path() + "/" + n)

                if os.getcwd() != get_flat_notes_path():
                    os.link(get_flat_notes_path() + "/" + n, n)

    def do_remove(self, args):
        arglist = shlex.split(args)
        args = get_remove_args(arglist)

        if args.permanent:
            temp_chdir_run(get_notes_path(), self.perm_remove, [args.paths])
            return

        for rgx in args.paths:
            if os.path.exists(rgx):
                if os.path.isdir(rgx) and not os.listdir(rgx):  # is an empty directory
                    os.rmdir(rgx)
                elif os.path.isdir(rgx) and args.recursive:
                    shutil.rmtree(rgx)
                elif os.path.isfile(rgx):
                    os.remove(rgx)
                else:
                    invalid()

    def do_mv(self, args):
        arglist = shlex.split(args)
        if len(arglist) != 2:
            print("Command 'mv' expects 2 arguments")
            return
        if not os.path.isdir(arglist[1]) and os.path.exists(arglist[1]):
            # If the target already exists and is not a directorys
            print("A file exists with the target path, aborting (no-clobber)")
            return

        try:
            # Check if the second argument is a file or a directory, if file perform a recursive rename and move
            old_name = os.path.basename(arglist[0])
            new_name = os.path.basename(arglist[1])

            if (
                os.path.isfile(arglist[0])
                and not os.path.exists(arglist[1])
                and old_name != new_name
            ):
                # We have a rename instead of a move
                if os.path.exists(get_flat_notes_path() + "/" + new_name):
                    print("A note already exists with the given name, aborting")
                    return

                temp_chdir_run(
                    get_notes_path(), self.recursive_rename, [old_name, new_name]
                )
                shutil.move(
                    os.path.dirname(os.path.abspath(arglist[0])) + "/" + new_name,
                    arglist[1],
                )
            else:
                shutil.move(arglist[0], arglist[1])
        except:
            invalid()

    def do_add(self, args):
        args = get_add_args(shlex.split(args))

        try:
            if args.path:
                temp_chdir_run(args.path, self.add_helper, [args.targets])
            else:
                self.add_helper(args.targets)
        except:
            invalid()

    def do_quit(self, args):
        sys.exit()

    def do_save(self, args):
        temp_chdir_run_list(
            get_notes_path(),
            [self.do_git] * 3,
            [["add ."], ['commit -m "Save"'], ["push"]],
        )

    def do_git(self, args):
        arglist = shlex.split(args)
        arglist.insert(0, get_git_path())
        run(arglist)

        # List of things to render in the UI

    def do_render(self, args):
        arglist = shlex.split(args)
        arglist.insert(0, get_dir_server_path())
        args = get_render_args(arglist)

        # Start the file server
        global hasStartedFileServer
        if not hasStartedFileServer and not args.view:
            # FIXME: implement this in a less confusing way later
            pid = spawn_quiet([get_dir_server_path(), "-d", get_notes_path()])
            reap_pid([pid])
            print("Server PID: ", pid)
            hasStartedFileServer = True

        # Serve the UI
        if args.debug and not args.attach:
            pid2 = spawn_quiet([
                "python3",
                "-m",
                "http.server",
                get_render_dbg_port(),
                "-d",
                get_ui_path(),
            ])
            reap_pid([pid2])
            open_default("http://localhost:" + get_render_dbg_port())
            print("UI PID: ", pid2)
        elif not args.attach:
            open_default("https://notes.davidpeet.me")

    def do_build(self, args):
        arglist = shlex.split(args)
        arglist.insert(0, get_preproc_path())
        arglist.insert(1, get_notes_path())
        run(arglist)

    def do_clean(self, args):
        temp_chdir_run(get_notes_path(), shutil.rmtree, ["build"])

    # Pythons regex lib is probably implemented in C++ anyway
    def do_search(self, args):
        args = get_search_args(shlex.split(args), [get_flat_notes_path()])
        fileMap = searchDirList(args.files, args.pattern, args.deep)

        # Sort deep search results by number of occurances
        for key, value in sorted(fileMap.items(), reverse=True, key=lambda x: x[1]):
            if int(value) > 0:
                print(key + ", " + str(value))

    def do_cp(self, args):
        arglist = shlex.split(args)
        if len(arglist) != 2:
            print("Incorrect number of arguments")
            return

        try:
            shutil.copy(os.path.expanduser(arglist[0]), os.path.expanduser(arglist[1]))
        except:
            print("Cannot copy.")

    def do_refs(self, args):
        arglist = shlex.split(args)
        args = get_refs_args(arglist)
        lower_bound = 0
        upper_bound = -1
        # -1 means unbounded

        if args.lower_bound:
            lower_bound = int(args.lower_bound)

        if args.upper_bound:
            upper_bound = int(args.upper_bound)

        if args.files:
            # print all references to a note in the base dir
            temp_chdir_run(get_notes_path(), self.get_refs, [args.files])
        elif args.lower_bound or args.upper_bound:
            # get refs for everything, print refs in given range
            refs_dict = {}  # Map file name to number of references
            temp_chdir_run(get_notes_path(), self.get_refs_in_range, [refs_dict])
            for entry in refs_dict:
                if refs_dict[entry] >= lower_bound and (
                    upper_bound == -1 or refs_dict[entry] <= upper_bound
                ):
                    print(entry, refs_dict[entry])
        else:
            print("Invalid command invocation")

    # -------------------- ALIASES -------------------

    def do_cr(self, args):
        "Alias for Create command"
        self.do_create(args)

    def do_b(self, args):
        "Alias for build command"
        self.do_build(args)

    def do_q(self, args):
        "Alias for quit"
        self.do_quit(args)

    def do_rm(self, args):
        "Alias for remove command"
        self.do_remove(args)

    def do_sv(self, args):
        "Alias for save command"
        self.do_save(args)

    def do_sr(self, args):
        "Alias for search command"
        self.do_search(args)

    def do_mkdir(self, args):
        "Alias for create --filter command"
        self.do_create("-f " + args)

    def do_touch(self, args):
        "Alias for create --note command"
        self.do_create("-n " + args)

    def do_rename(self, args):
        "Alias for mv"
        self.do_mv(args)

    # ------------- AUTO COMPLETE --------------

    def complete_ls(self, text, line, startIdx, endIdx):
        return self.dir_complete(text, line, startIdx, endIdx)

    def complete_cat(self, text, line, startIdx, endIdx):
        return self.file_dir_complete(text, line, startIdx, endIdx)

    def complete_cd(self, text, line, startIdx, endIdx):
        return self.dir_complete(text, line, startIdx, endIdx)

    def complete_add(self, text, line, startIdx, endIdx):
        return self.note_complete(text, line, startIdx, endIdx)

    def complete_remove(self, text, line, startIdx, endIdx):
        return self.file_dir_complete(text, line, startIdx, endIdx)

    def complete_rm(self, text, line, startIdx, endIdx):
        return self.complete_remove(text, line, startIdx, endIdx)

    def complete_rename(self, text, line, startIdx, endIdx):
        return self.file_dir_complete(text, line, startIdx, endIdx)

    def complete_edit(self, text, line, startIdx, endIdx):
        return self.note_complete(text, line, startIdx, endIdx)

    def complete_mv(self, text, line, startIdx, endIdx):
        return self.file_dir_complete(text, line, startIdx, endIdx)

    def complete_refs(self, text, line, startIdx, endIdx):
        return self.note_complete(text, line, startIdx, endIdx)

    # ---------------- DOCS --------------------

    def help_init():
        print(
            "Initialize directories needed for this application to function as required."
        )

    def help_rename():
        print("Rename src to dest")

    def help_edit():
        print("Opens the specified file or directory path in sublime text")

    def help_cat():
        print("Print out the contents of the argument file path")

    def help_ls():
        print(
            """
List contents of directory, defaults to current directory.
Syntax: ls [optional filter path]
		"""
        )

    def help_cd():
        print("Used to navigate within the file system.\nSyntax: cd <filter path>")

    def help_mv():
        print("Move a file from src to dest")

    def help_cp():
        print("Copy a file from src to dest")

    def help_create():
        print(
            """
Command for creating new filters or notes.
This command is aliased by the command 'cr'
Syntax:
create [--filter/-f] [ list of filter paths ]
create [--note/-n] [ list of note paths ]
		"""
        )

    def help_remove():
        print(
            """
Removes all files matching given paths from the current filter.
Note that notes removed without the -p flag still exist in .flat_notes
This command is aliased by the command 'rm'
Flags:
-r allows recursive removal of directories matched
-p permanantly removal of all instances of the note (recursive removal from ~/.notes)
Syntax:
remove [file list]
remove -r [file list]
remove -p [file list]
		"""
        )

    def help_quit():
        print("Quit the command line interface")

    def help_save():
        print(
            "Saves the base ~/.notes directory to github.\nRequires that a git repo has already been set up in ~/.notes"
        )

    def help_build():
        print(
            """
Preprocess notes and send them to the build directory.
The build command is aliased by the command 'b'
		"""
        )

    def help_add():
        print(
            """
The add command adds existing notes by NAME (not by path) to the current filter / directory
Flags:
-p --> indicate the path of the filter to add to instead of adding to .
Syntax:
add -p <filter path> [ list of notes ]
add [ list of notes ]
		"""
        )

    def help_search():
        print(
            """
Search by default will search for matching note names.
All patterns must be provided as Regex conforming to the ECMA Script standard.
The search command is aliased by 'sr'
Flags:
-d --> searches the contents of files instead of their file names
Syntax:
search [pattern]
search -d [pattern] [list of files / directories to search in - defaults to .notes/.flat_notes]
		"""
        )

    def help_clean():
        print(
            "Clean command removes the build directory so that everything may be rebuild from scratch"
        )

    def help_git():
        print("The Git command allows performing git commands, syntax is as usual")

    def help_render():
        print("Render target files in the Angular UI")

    # ---------------- OVERRIDES ---------------

    def postcmd(self, stop, line):
        self.prompt = get_prompt(
            self.promptBase, self.promptPath, self.promptTerminator
        )

    def default(self, line):
        print("Unrecognized Command.")

    # ---------------- HELPERS ----------------

    def recursive_rename(self, old_name, new_name):
        # Requires that we start in root notes directory
        dirlist = os.scandir()

        for file in dirlist:
            if file.is_dir():
                temp_chdir_run(file.path, self.recursive_rename, [old_name, new_name])
            elif file.name == old_name:
                print("Renaming ", os.getcwd() + "/" + file.name)
                shutil.move(old_name, new_name)

    def add_helper(self, arglist):
        for file in arglist:
            os.link(get_flat_notes_path() + "/" + file, "./" + file)

    def perm_remove(self, arglist):
        arr = os.scandir(".")

        for file in arr:
            if file.is_dir():
                temp_chdir_run(file.name, self.perm_remove, [arglist])
            elif file.name in arglist:
                self.do_remove(file.name)

    def cat_helper(self, arg):
        try:
            fd = open(arg, "r")
            text = fd.read()
            fd.close()
            return text
        except:
            invalid(
                "Cannot cat, check that file exists and that you have read permission."
            )
            return ""

    def edit_files(self, arglist):
        args = get_edit_args(arglist)
        cmd = args.command

        for p in args.paths:
            if not os.path.exists(p):
                shouldCreate = input(
                    "Note "
                    + p
                    + " does not exist, do you want to create it in .flat_notes? [y/n]"
                )
                if shouldCreate.lower().strip() == "y":
                    self.do_create("-n " + p)

        if args.paths and not cmd:
            open_default(" ".join(args.paths))
        elif args.paths:
            args.paths.insert(0, cmd)
            spawn_quiet(args.paths)

    def get_refs(self, arglist):
        dirlist = os.scandir()

        patterns = [];

        for pattern in arglist:
          patterns.append(re.compile(pattern));

        for file in dirlist:
            if (
              file.is_dir()
              and file.name != "build"
              and (not file.name.startswith(".") or file.name == ".flat_notes")
            ):
                temp_chdir_run(file.path, self.get_refs, [arglist])
            elif not file.is_dir() and not file.name.startswith("."):
                match = False;
                for pattern in patterns:
                  match |= pattern.match(file.name) != None
                if match:
                  print(os.path.relpath(file.path, start=get_notes_path()))

    def get_refs_in_range(self, ref_dict):
        flist = os.scandir()

        for file in flist:
            if (
                file.is_dir()
                and file.name != "build"
                and (not file.name.startswith(".") or file.name == ".flat_notes")
            ):
                temp_chdir_run(file.path, self.get_refs_in_range, [ref_dict])
            elif not file.is_dir() and not file.name.startswith("."):
                if file.name in ref_dict:
                    ref_dict[file.name] += 1
                else:
                    ref_dict[file.name] = 1

    def get_word_at_index(self, text, index):
        # Extract string including startIndex
        tokens = re.split(" ", text)
        length = 0
        for token in tokens:
            length += len(token)
            if index <= length:
                return token
        return ""

    def complete_abs(self, fullpath, cond):
        if fullpath:
            return [
                os.path.basename(entry.path)
                for entry in dir_contents(fullpath)
                if cond(entry) and entry.name.startswith(os.path.basename(fullpath))
            ]
        elif fullpath.startswith("/"):
            return [
                os.path.basename(entry.path)
                for entry in dir_contents(fullpath[1:], get_notes_path())
                if cond(entry) and entry.name.startswith(os.path.basename(fullpath))
            ]
        else:
            return [
                os.path.basename(entry.path)
                for entry in dir_contents(fullpath)
                if cond(entry)
            ]

    def file_complete(self, text, line, startIdx, endIdx):
        fullpath = self.get_word_at_index(line, startIdx)

        return self.complete_abs(fullpath, lambda entry: entry.is_file())

    def dir_complete(self, text, line, startIdx, endIdx):
        fullpath = self.get_word_at_index(line, startIdx)

        return self.complete_abs(fullpath, lambda entry: entry.is_dir())

    def file_dir_complete(self, text, line, startIdx, endIdx):
        fullpath = self.get_word_at_index(line, startIdx)

        return self.complete_abs(
            fullpath, lambda entry: entry.is_dir()
        ) + self.complete_abs(fullpath, lambda entry: entry.is_file())

    def file_dir_note_complete(self, text, line, startIdx, endIdx):
        return self.file_dir_complete(
            text, line, startIdx, endIdx
        ) + self.note_complete(text, line, startIdx, endIdx)

    def note_complete(self, text, line, startIdx, endIdx):
        if text:
            return [
                os.path.basename(entry.path)
                for entry in dir_contents(
                    os.path.expanduser(get_flat_notes_path()) + "/"
                )
                if entry.name.startswith(os.path.basename(text))
            ]
        else:
            arr = dir_contents(os.path.expanduser(get_flat_notes_path()) + "/")
            for entry in arr:
                if entry.name.startswith(os.path.basename(text)):
                    print(entry.name)


# Start the CLI if this is the main process
if __name__ == "__main__":
    NoteShell().cmdloop()
