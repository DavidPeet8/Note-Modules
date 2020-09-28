#! /usr/bin/python3

import cmd, sys, os, shutil, re
import collections
import shlex
from fs_helpers import *
from config import *
from color_scheme import print_dir, get_prompt
from process_manager import reap_pid, open_default, spawn, spawn_quiet, run, spawn_attach_stdout
from argparser import *

sys.path.insert(1, os.path.expanduser("~/.notes_cfg/.exe/searchLib"))
from search import searchDirList, dumpMap

hasStartedFileServer = False

args = get_driver_args(sys.argv[1:])

if args.path:
	update_base_path(args.path)

if not os.path.isdir(get_base_path()):
	os.mkdir(get_base_path())
os.chdir(get_base_path()) # Set working directory to base of notes directory


def invalid(reason=""):
	print("Invalid Command.")
	if reason != "":
		print(reason)

class NoteShell (cmd.Cmd):

	def __init__(self):
		cmd.Cmd.__init__(self)
		self.intro = '''
Welcome to NoteShell.
Author: David Peet
Github: davidpeet8
Type help or ? for a list of commands.
		'''
		self.promptBase = "(NoteShell) " 
		self.promptPath = ""
		self.promptTerminator = ": "
		self.prompt = get_prompt(self.promptBase, self.promptPath, self.promptTerminator)

	# should recieve no arguments
	def do_init(self, arg):
		check_and_mkdirs([get_flat_notes_path(), get_base_path()+"/build", get_base_path() + "/.config", get_base_path() + "/.assets"])
		temp_chdir_run(get_base_path(), self.do_git, ["init"])


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
				if not isAll and entry.name.startswith('.'): 
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
			os.chdir(arg)
			promptPath = os.getcwd().split('.notes',1)
			self.promptPath = promptPath[1] if isinstance(promptPath, list) and len(promptPath) > 1 else "/"
		except:
			invalid('Check that the filter exists, and that you have execute permission')

	def do_create(self, args):
		arglist = shlex.split(args)

		args = get_create_args(arglist)
		if not args.filter and not args.note:
			invalid("Must specify -f or -n")
			return
		elif (args.filter and len(args.filter) < 1) or (args.note and len(args.note) < 1):
			invalid("Both -f and -n require an argument")

		if args.filter:
			for f in args.filter:
				check_and_mkdir(f)
			
		if args.note:
			for n in args.note:
				if os.path.exists(get_flat_notes_path() + '/' + n):
					print('A note of this name already exists in .flat_notes')
					print('To add this note to the specified directory use the add command')
					print('To remove this file permanantly use the remove command with the -p flag')
					continue
				touch_file(get_flat_notes_path() + '/' + n)

				if os.getcwd() != get_flat_notes_path():
					os.link(get_flat_notes_path() + '/' + n, n)
		

	def do_remove(self, args):
		arglist = shlex.split(args)
		args = get_remove_args(arglist)
		
		if args.permanent:
			temp_chdir_run(get_base_path(), self.perm_remove, [args.paths])
			return			

		for rgx in args.paths:
			if os.path.exists(rgx):
				if os.path.isdir(rgx) and not os.listdir(rgx): # is an empty directory
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
		try:
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
		temp_chdir_run_list(get_base_path(), [self.do_git]*3, [["add ."], ["commit -m \"Save\""], ["push"]])
		
	def do_git(self, args):
		GITEXE = "git"
		arglist = shlex.split(args)
		arglist.insert(0, GITEXE)
		run(arglist)

		# List of things to render in the UI

	def do_render(self, args):
		arglist = shlex.split(args)
		arglist.insert(0, SERVER_EXE)
		args = get_render_args(arglist)

		# Start the file server
		global hasStartedFileServer
		if not hasStartedFileServer and not args.view:
			pid = spawn_quiet(arglist)
			reap_pid([pid])
			print("Server PID: ", pid)
			hasStartedFileServer = True;

		# Serve the UI
		if args.debug and not args.attach:
			pid2 = spawn_quiet(["python3", "-m", "http.server", RENDER_PORT, "-d", UI_EXE])
			reap_pid([pid2])
			open_default("http://localhost:" + RENDER_PORT)
			print("UI PID: ", pid2)
		elif not args.attach:
			open_default("https://davidpeet8.github.io/Note-Modules")
		
		

	def do_build(self, args):
		arglist = shlex.split(args)
		arglist.insert(0, PREPROCESSOR_EXE)
		arglist.insert(1, get_base_path())
		run(arglist)

	def do_clean(self, args):
		temp_chdir_run(get_base_path(), shutil.rmtree, ["build"])


	# Might be a better idea to just make a python executable for searching
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
		# print all references to a note in the base dir
		rawarglist = shlex.split(args)
		temp_chdir_run(get_base_path(), self.get_refs, [rawarglist])


	# -------------------- ALIASES -------------------

	def do_cr(self, args):
		'Alias for Create command'
		self.do_create(args) 

	def do_b(self, args):
		'Alias for build command'
		self.do_build(args)

	def do_q(self, args):
		'Alias for quit'
		self.do_quit(args)

	def do_rm(self, args):
		'Alias for remove command'
		self.do_remove(args)

	def do_sv(self, args):
		'Alias for save command'
		self.do_save(args)

	def do_sr(self, args):
		'Alias for search command'
		self.do_search(args)

	def do_mkdir(self, args):
		'Alias for create --filter command'
		self.do_create("-f " + args)

	def do_touch(self, args):
		'Alias for create --note command'
		self.do_create("-n " + args)

	def do_rename(self, args):
		'Alias for mv'
		self.do_mv(args)

	# ------------- AUTO COMPLETE --------------
	
	def complete_ls(self, text, line, startIdx, endIdx):
		return self.dir_complete(text, line, startIdx, endIdx)

	def complete_cat(self, text, line, startIdx, endIdx):
		return self.file_complete(text, line, startIdx, endIdx)

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
		return self.file_dir_note_complete(text, line, startIdx, endIdx)

	def complete_mv(self, text, line, startIdx, endIdx):
		return self.file_dir_complete(text, line, startIdx, endIdx)

	def complete_refs(self, text, line, startIdx, endIdx):
		return self.note_complete(text, line, startIdx, endIdx)

	# ---------------- DOCS --------------------

	def help_init():
		print('Initialize directories needed for this application to function as required.')

	def help_rename():
		print("Rename src to dest")

	def help_edit():
		print('Opens the specified file or directory path in sublime text')

	def help_cat():
		print('Print out the contents of the argument file path')

	def help_ls():
		print('''
List contents of directory, defaults to current directory.
Syntax: ls [optional filter path]
		''')

	def help_cd():
		print('Used to navigate within the file system.\nSyntax: cd <filter path>')

	def help_mv():
		print('Move a file from src to dest')

	def help_cp():
		print('Copy a file from src to dest')

	def help_create():
		print('''
Command for creating new filters or notes.
This command is aliased by the command 'cr'
Syntax: 
create [--filter/-f] [ list of filter paths ]
create [--note/-n] [ list of note paths ]
		''')

	def help_remove():
		print('''
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
		''')

	def help_quit():
		print('Quit the command line interface')

	def help_save():
		print('Saves the base ~/.notes directory to github.\nRequires that a git repo has already been set up in ~/.notes')

	def help_build():
		print('''
Preprocess notes and send them to the build directory.
The build command is aliased by the command 'b'
		''')

	def help_add():
		print('''
The add command adds existing notes by NAME (not by path) to the current filter / directory
Flags:
-p --> indicate the path of the filter to add to instead of adding to .
Syntax:
add -p <filter path> [ list of notes ]
add [ list of notes ]
		''')

	def help_search():
		print('''
Search by default will search for matching note names.
All patterns must be provided as Regex conforming to the ECMA Script standard.
The search command is aliased by 'sr'
Flags:
-d --> searches the contents of files instead of their file names
Syntax:
search [pattern]
search -d [pattern] [list of files / directories to search in - defaults to .notes/.flat_notes]
		''')

	def help_clean():
		print('Clean command removes the build directory so that everything may be rebuild from scratch')

	def help_git():
		print('The Git command allows performing git commands, syntax is as usual')

	def help_render():
		print('Render target files in the Angular UI')

	# ---------------- OVERRIDES ---------------

	def postcmd(self, stop, line):
		self.prompt = get_prompt(self.promptBase, self.promptPath, self.promptTerminator)

	def default(self, line):
		print("Unrecognized Command.")

	# ---------------- HELPERS ----------------

	def add_helper(self, arglist):
		for file in arglist:
			os.link(get_flat_notes_path() + "/" + file, './' + file)

	def perm_remove(self, arglist):
		arr = os.scandir('.')

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
			invalid("Cannot cat, check that file exists and that you have read permission.")
			return ""

	def edit_files(self, arglist):
		cmd = ""
		args = get_edit_args(arglist)
		if args.command:
			cmd = args.command

		for p in args.paths:
			if not os.path.exists(p):
				shouldCreate = input("Note " + p + " does not exist, do you want to create it in .flat_notes? [y/n]")
				if shouldCreate.lower().strip() == "y":
					self.do_create("-n " + p)

		if args.paths and not cmd:
			open_default(' '.join(args.paths))
		elif args.paths:
			args.paths.insert(0, cmd)
			spawn_quiet(args.paths)

	def get_refs(self, arglist):
		dirlist = os.scandir()

		for file in dirlist:
			if file.is_dir() and file.name != ".flat_notes" and file.name != "build":
				temp_chdir_run(file.path, self.get_refs, [arglist])
			elif file.name in arglist:
				print(os.path.relpath(file.path, start=get_base_path()))

	def file_complete(self, text, line, startIdx, endIdx):
		if text:
			return [
				entry.path for entry in dir_contents(text)
				if entry.is_file() and entry.name.startswith(os.path.basename(text))
			]
		else: 
			print(entry.path for entry in dir_contents(text) if entry.is_file())

	def dir_complete(self, text, line, startIdx, endIdx):
		if text:
			return [
				entry.path for entry in dir_contents(text)
				if entry.is_dir() and entry.name.startswith(os.path.basename(text))
			]
		else: 
			print(entry.path for entry in dir_contents(text) if entry.is_dir())

	def file_dir_complete(self, text, line, startIdx, endIdx):
		if text:
			return [
				entry.path for entry in dir_contents(text)
				if (entry.is_dir() or entry.is_file()) and entry.name.startswith(os.path.basename(text))
			]
		else: 
			print(entry.path for entry in dir_contents(text) if entry.is_dir() or entry.is_file())

	def file_dir_note_complete(self, text, line, startIdx, endIdx):
		return self.file_dir_complete(text, line, startIdx, endIdx) + self.note_complete(text, line, startIdx, endIdx);

	def note_complete(self, text, line, startIdx, endIdx):
		if text:
			return [
				os.path.basename(entry.path) for entry in dir_contents(os.path.expanduser(get_flat_notes_path()) + "/") 
				if entry.name.startswith(os.path.basename(text))
			]
		else:
			print(os.path.basename(entry.path) for entry in dir_contents(os.path.expanduser(get_flat_notes_path()) + "/"))

# Start the CLI if this is the main process
if __name__ == '__main__':
	NoteShell().cmdloop()