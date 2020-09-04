#! /usr/bin/python3
# CLI Driver for note CLI
# Maybe switch to using the subprocess module

import cmd, sys, os, shutil, re
import collections
from colorama import init, Fore, Back, Style
import atexit, signal
import webbrowser
import subprocess
import shlex
from fs_helpers import *
init()

basePath = os.path.expanduser("~/.notes")
flatNotesPath = os.path.expanduser("~/.notes/.flat_notes")
textEditorCMD = "subl"
promptColor = Fore.CYAN + Style.BRIGHT

PREPROCESSOR_EXE = basePath + "/.exe/preprocessor"
SERVER_EXE = basePath + "/.exe/dirServer/server.py"
UI_EXE = basePath + "/.exe/UI"
RENDER_PORT = "4300"
arPID = []

def invalid(reason=""):
	print("Invalid Command.")
	if reason != "":
		print(reason)

# reap all children onexit
def reap():
	for pid in arPID:
		os.kill(pid, signal.SIGKILL)

def reset_print_style():
	print(Style.RESET_ALL, end="")

atexit.register(reap)

class NoteShell (cmd.Cmd):
	intro = '''
Welcome to NoteShell.
Author: David Peet
Github: davidpeet8
Type help or ? for a list of commands.
	'''
	promptBase = promptColor + "(NoteShell) " 
	promptPath = ""
	propmptTerminator = ": " + Style.RESET_ALL
	prompt = promptColor + "(NoteShell) : " + Style.RESET_ALL

	# should recieve no arguments
	def do_init(self, arg):
		check_and_mkdirs([flatNotesPath, basePath+"/build", basePath + "/.config", basePath + "/.exe"])
		temp_chdir_run(basePath, self.do_git, ["init"])


	# Directory to open in text editor
	def do_edit(self, args):
		rawarglist = shlex.split(args)
		temp_chdir_run(flatNotesPath, self.edit_files, [rawarglist])
		

	def do_ls(self, args):
		arglist = shlex.split(args)
		firstArg = arglist[0].lower() if arglist else ""
		isAll, arr = False, []

		try:
			if firstArg != "":
				if firstArg == "-a" or firstArg == "--all":
					isAll = True
					dirPath = arglist[1] if len(arglist) > 1 and arglist[1] else "."
					arr = os.scandir(dirPath)
				elif firstArg == "-n" or firstArg == "--notes":
					arr = os.scandir(flatNotesPath)
				else:
					arr = os.scandir(args)
			else: 
				arr = os.scandir(".")

			for entry in arr:
				if isAll == False and entry.name.startswith('.'): 
					continue
				if entry.is_dir():
					print(Fore.BLUE + Style.BRIGHT + entry.name)
					reset_print_style()
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

		if arglist and len(arglist) >= 2:
			firstArg = arglist[0].lower()
			if firstArg == '-f' or firstArg == '--filter':
				# Create the new filters
				for f in arglist[1:]:
					check_and_mkdir(f)
				return
			elif firstArg == '-n' or firstArg == '--note':
				# Create the new notes
				for n in arglist[1:]:
					if os.path.exists(flatNotesPath + '/' + n):
						print('A note of this name already exists in .flat_notes')
						print('To add this note to the specified directory use the add command')
						print('To remove this file permanantly use the remove command with the -p flag')
						return
					touch_file(flatNotesPath + '/' + n)

					if os.getcwd() != flatNotesPath:
						os.link(flatNotesPath + '/' + n, n)
				return
		invalid("Create command requires at least 2 arguments")

	def do_remove(self, args):
		arglist = shlex.split(args)
		i, recursive = 0, False
		firstArg = arglist[0].lower() if arglist else ""

		if firstArg == "-r" or firstArg == "--recursive":
			i,recursive = 1,True

		if firstArg == "-p" or firstArg == "--permanent":
			temp_chdir_run(basePath, self.perm_remove, arglist[1:])

		for rgx in arglist[i:]:
			if os.path.exists(rgx):
				if os.path.isdir(rgx) and not os.listdir(rgx): # is an empty directory
					os.rmdir(rgx)
				elif os.path.isdir(rgx) and recursive:
					shutil.rmtree(rgx)
				elif os.path.isfile(rgx):
					os.remove(rgx)
				else:
					invalid()

	def do_rename(self, args):
		arglist = shlex.split(args)
		if len(args) != 2:
			print("Command 'mv' expects 2 arguments")
			return
		try:
			os.rename(args[0], args[1])
		except: 
			invalid()


	def do_add(self, args):
		arglist = shlex.split(args)
		firstArg = arglist[0].lower() if arglist else ""
	
		try:
			if firstArg == "-p" or firstArg == '--path':
				temp_chdir_run(arglist[1], self.add_helper, arglist[2:])
			else: 
				self.add_helper(arglist)
		except:
			invalid()

	def do_quit(self, args):
		sys.exit()

	def do_save(self, args):
		temp_chdir_run_list(basePath, [self.do_git]*3, [["add ."], ["commit -m \"Save\""], ["push"]])
		
	def do_git(self, args):
		GITEXE = "git"
		arglist = shlex.split(args)
		arglist.insert(0, GITEXE)
		subprocess.run(arglist)

		# List of things to render in the UI

	def do_render(self, args):
		arglist = shlex.split(args)
		arglist.insert(0, SERVER_EXE)
		global arPID

		# Start the file server
		pid = subprocess.Popen(arglist, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).pid
		# Serve the UI
		pid2 = subprocess.Popen(["python3", "-m", "http.server", RENDER_PORT, "-d", UI_EXE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).pid
		arPID += [pid, pid2]
		webbrowser.open("http://localhost:" + RENDER_PORT)
		print("Server PID: ", pid)
		print("UI PID: ", pid2)

	def do_build(self, args):
		arglist = shlex.split(args)
		arglist.insert(0, PREPROCESSOR_EXE)
		arglist.insert(1, basePath)
		subprocess.run(arglist)

	def do_clean(self, args):
		temp_chdir_run(basePath, shutil.rmtree, ["build"])

	def do_search(self, args):
		arglist = shlex.split(args)
		firstArg = arglist[0].lower() if arglist else ""
		fileMap = {}

		if (firstArg == "-d" or firstArg == "--deep") and len(arglist) == 3:
			pattern = arglist[1]
			searchFiles = arglist[2:] if arglist[2:] else [flatNotesPath] # Files / Dirs to search in
			
			for path in searchFiles:
				path = os.path.expanduser(path)
				if os.path.exists(path) and os.path.isdir(path):
					fileMap = {**fileMap, **self.search_dir(pattern, os.scandir(path))}
				elif os.path.exists(path):
					fileMap[path] = search_file(pattern, path)
				else: 
					print("File path given does not exist. Run 'help search' for details on the search command.")

			# Sort deep search results by number of occurances
			for key, value in sorted(fileMap.items(), reverse=True, key=lambda x: x[1]):
				print("["+ key + ", " + str(value) + "]")

		elif len(arglist) == 1: # Search only by file name
			notes = os.listdir(flatNotesPath)
			pattern = arglist[0]

			for note in notes:
				if re.search(pattern, note, re.IGNORECASE):
					print(note)
		else: 
			invalid("Incorrect Number of arguments")

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
		return self.file_dir_complete(text, line, startIdx, endIdx)

	def complete_rename(self, text, line, startIdx, endIdx):
		return self.file_dir_complete(text, line, startIdx, endIdx)

	def complete_edit(self, text, line, startIdx, endIdx):
		return self.file_dir_note_complete(text, line, startIdx, endIdx)

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
		self.prompt = self.promptBase + self.promptPath + self.propmptTerminator

	def default(self, line):
		print("Unrecognized Command.")

	# ---------------- HELPERS ----------------

	def add_helper(self, arglist):
		for file in arglist:
			os.link(flatNotesPath + "/" + file, './' + file)

	def perm_remove(self, arglist):
		arr = os.scandir(".")
		for file in arr:
			if file.is_dir():
				temp_chdir_run(file.name, self.perm_remove, arglist)
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

	def edit_files(self, rawarglist):
		arglist = []
		for p in rawarglist:
			if os.path.exists(p):
				arglist += [p]
			else:
				shouldCreate = input("Note " + p + " does not exist, do you want to create it in .flat_notes? [y/n]")
				if shouldCreate.lower().strip() == "y":
					self.do_create("-n " + p)
					arglist += [p]

		if arglist:
			arglist.insert(0, textEditorCMD)
			pid = subprocess.Popen(arglist, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).pid

	def search_file(self, pattern, path):
		fd = open(path, "r")
		text = fd.read()
		fd.close()
		return len(re.findall(pattern, text, re.IGNORECASE))

	def search_dir(self, pattern, filelist):
		results = {}
		for file in filelist:
			if os.path.isdir(file.path):
				if not file.name.startswith("."): 
					results = {**results, **self.search_dir(pattern, os.scandir(file.path))}
			else:
				results[file.path] = self.search_file(pattern, file.path);
		return results

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
		print("File Dir COmplete")

	def file_dir_note_complete(self, text, line, startIdx, endIdx):
		print("FIle Dir Note COmplete")

	def note_complete(self, text, line, startIdx, endIdx):
		if text:
			return 

if not os.path.isdir(basePath):
	os.mkdir(basePath)
os.chdir(basePath) # Set working directory to base of notes directory

# Start the CLI if this is the main process
if __name__ == '__main__':
	NoteShell().cmdloop()

