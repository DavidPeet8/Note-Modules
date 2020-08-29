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
init()

basePath = os.path.expanduser("~/.notes")
flatNotesPath = os.path.expanduser("~/.notes/.flat_notes")
textEditorCMD = "subl"
promptColor = Fore.CYAN + Style.BRIGHT

PREPROCESSOR_EXE = basePath + "/.exe/preprocessor"
SERVER_EXE = basePath + "/.exe/dirServer/server.py"
UI_EXE = basePath + "/.exe/UI"
arPID = []

def invalid(reason=""):
	print("Invalid Command.")
	if reason != "":
		print(reason)

# reap all children onexit - this may prevent exit from process 
def reap():
	for pid in arPID:
		os.kill(pid, signal.SIGKILL)

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
		'Initialize directories needed for this application to function as required'
		if not os.path.isdir(flatNotesPath):
			os.mkdir(flatNotesPath)
		if not os.path.isdir(basePath + "/build"):
			os.mkdir(basePath + "/build")
		if not os.path.isdir(basePath+ "/.config"):
			os.mkdir(basePath + "/.config")
		if not os.path.isdir(basePath+ "/.exe"):
			os.mkdir(basePath + "/.exe")
		cwd = os.getcwd();
		os.chdir(basePath) # Go to root directory
		self.do_git("init") # initialize a git repository
		os.chdir(cwd) # change back to the previous directory


	# Directory to open in text editor
	def do_edit(self, args):
		'Opens the specified file or directory in sublime text'
		arglist = shlex.split(args)
		filelist = []
		
		cwd = os.getcwd()
		os.chdir(flatNotesPath)
		for p in arglist:
			if not os.path.exists(p):
				shouldCreate = input("Note " + p + " does not exist, do you want to create it in .flat_notes? [y/n]")
				if shouldCreate.lower().strip() == "y":
					self.do_create("-n " + p)
					filelist += [p]
			else:
				filelist += [p]

		if filelist:
			filelist.insert(0, textEditorCMD)
			subprocess.run(filelist, close_fds = True)
		os.chdir(cwd)

	def do_ls(self, args):
		'List contents of current directory'
		arglist = shlex.split(args)
		firstArg = arglist[0].lower() if arglist else ""
		isAll = False

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
					print(Style.RESET_ALL, end="")
				else:
					print(entry.name)
		except:
			invalid()

	def do_cat(self, args):
		'Print out the contents of the argument file'
		text = self._cat_helper(args)

		if text != "":
			print(text)

	def do_cd(self, arg):
		'Navigate within stored notes'
		try:
			os.chdir(arg)
			promptPath = os.getcwd().split('.notes',1)
			self.promptPath = promptPath[1] if isinstance(promptPath, list) and len(promptPath) > 1 else "/"
		except:
			invalid()

	def do_create(self, args):
		'''
		Command for creating new filters or notes.
		To create a filter - create filter <filter_path>
		To create a note - create note <note_path>
		'''
		arglist = shlex.split(args)

		if arglist and len(arglist) >= 2:
			firstArg = arglist[0].lower()
			if firstArg == '-f' or firstArg == '--filter':
				# Create the new filters
				for f in arglist[1:]:
					try:
						os.mkdir(f)
					except:
						print("Filter Already Exists.")
				return
			elif firstArg == '-n' or firstArg == '--note':
				# Create the new notes
				for n in arglist[1:]:
					if os.path.exists(flatNotesPath + '/' + n):
						invalid()
						print('A note of this name already exists in .flat_notes')
						print('To add this note to the specified directory use the add command.')
						print('To remove this file permanantly use the remove command.')
						return
					fd = open(flatNotesPath + '/' + n,"a+")
					fd.write("")
					fd.close()

					try:
						if os.getcwd() != flatNotesPath:
							os.link(flatNotesPath + '/' + n, n)
					except: 
						print("Note Already Exists.")
				return
		invalid("Unspecified Creation Type.")

	def do_remove(self, args):
		'''
		Remove all files matching given paths from the current filter
		-r flag allows recursive removal of directories matched
		-p flag allows permanant removal of a note, remove all instances of the note within the notes directory
		'''
		arglist = shlex.split(args)
		i, recursive = 0, False
		firstArg = arglist[0].lower() if arglist else ""

		if firstArg == "-r" or firstArg == "--recursive":
			i = 1
			recursive = True

		if firstArg == "-p" or firstArg == "--permanent":
			# Go to root directory and walk through removng all occurances
			cwd = os.getcwd();
			os.chdir(basePath) # Go to root directory
			self._perm_remove(arglist[1:])
			os.chdir(cwd) # change back to the previous directory

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

	def do_add(self, args):
		'''
		Add an existing notes by NAME not by path to target filter
		add p <path to add to> [ list of files ]
		add [ list of files ] 	--> (added to .)
		'''
		arglist = shlex.split(args)
		firstArg = arglist[0].lower() if arglist else ""
	
		try:
			if firstArg == "-p" or firstArg == '--path':
				cwd = os.getcwd();
				os.chdir(arglist[1]) # Go to root directory
				self._add_helper(arglist[2:])
				os.chdir(cwd) # change back to the previous directory
			else: 
				self._add_helper(arglist)

		except:
			invalid()

	def do_quit(self, args):
		'Quit the command line interface'
		sys.exit()

	def do_save(self, args):
		'Save the notes to github'
		self.do_git("add .")
		self.do_git("commit -m \"Save\"")
		self.do_git("push")

	def do_git(self, args):
		'Allow performing git commands, syntax as usual'
		GITEXE = "git"
		arglist = shlex.split(args)
		arglist.insert(0, GITEXE)
		subprocess.run(arglist)

		# List of things to render in the UI
	def do_render(self, args):
		'Render target files in the Angular UI'
		arglist = shlex.split(args)
		arglist.insert(0, SERVER_EXE)
		port = "4300"
		global arPID

		pid = subprocess.Popen(arglist, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).pid
		pid2 = subprocess.Popen(["python3", "-m", "http.server", port, "-d", UI_EXE], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).pid
		arPID += [pid, pid2]
		webbrowser.open("http://localhost:" + port)
		print("Server PID: ", pid)
		print("UI PID: ", pid2)

	def do_build(self, args):
		'Preprocess notes and send them to the build directory'
		arglist = shlex.split(args)
		print(arglist)
		arglist.insert(0, PREPROCESSOR_EXE)
		arglist.insert(1, basePath)
		pid = os.spawnvp(os.P_WAIT, PREPROCESSOR_EXE, arglist) # This will terminate of it's own accord, no need to be reaped

	def do_clean(self, args):
		cwd = os.getcwd()
		os.chdir(basePath)
		shutil.rmtree("build")
		os.chdir(cwd)

	def do_search(self, args):
		'''
		Search for notes. 
		Use the -d flag for a deep search including the bodies of each file
		search [-d] pattern [dir to search in]
		'''
		arglist = shlex.split(args)
		firstArg = arglist[0].lower() if arglist else ""
		fileMap = {}
		if (firstArg == "-d" or firstArg == "--deep") and len(arglist) >=3:
			# Start the Deep search process
			pattern = arglist[1]
			searchFiles = arglist[2:]
			
			for path in searchFiles:
				path = os.path.expanduser(path)
				if os.path.exists(path) and os.path.isdir(path):
					fileMap = {**fileMap, **self.search_dir(pattern, os.scandir(path))}
				elif os.path.exists(path):
					fileMap[path] = search_file(pattern, path)
				else: 
					print("File path given does not exist. Run 'help search' for details on the search command.")

			for key, value in sorted(fileMap.items(), reverse=True, key=lambda x: x[1]):
				print("["+ key + ", " + str(value) + "]")

		elif len(arglist) >= 1:
			# Just run a quick file name search
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

	# ---------------- OVERRIDES ---------------

	def postcmd(self, stop, line):
		self.prompt = self.promptBase + self.promptPath + self.propmptTerminator

	# ---------------- HELPERS ----------------
	def _add_helper(self, arglist):
		'''
		Should only be called by do_add 
		'''
		for file in arglist:
			os.link(flatNotesPath + "/" + file, './' + file)

	def _perm_remove(self, arglist):
		cwd = os.getcwd();
		arr = os.scandir(".")
		for file in arr:
			if file.is_dir():
				os.chdir(file.name)
				self._perm_remove(arglist)
				os.chdir(cwd)
			elif file.name in arglist:
				self.do_remove(file.name)

	def _cat_helper(self, args):
		try:
			fd = open(args, "r")
			text = fd.read()
			fd.close()
			return text
		except: 
			invalid("Cannot cat, check that file exists and that you have read permission.")
			return ""

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

	def cur_dir_contents(self):
		return os.scandir(os.getcwd())

	def file_complete(self, text, line, startIdx, endIdx):
		if text:
			return [
				entry.name for entry in self.cur_dir_contents()
				if entry.is_file() and entry.name.startswith(text)
			]
		else: 
			return [
				entry.name for entry in self.cur_dir_contents()
				if entry.is_file()
			]
			
	def dir_complete(self, text, line, startIdx, endIds):
		if text:
			return [
				entry.name for entry in self.cur_dir_contents()
				if entry.is_dir() and entry.name.startswith(text)
			]
		else: 
			return [
				entry.name for entry in self.cur_dir_contents()
				if entry.is_dir()
			]

if not os.path.isdir(basePath):
	os.mkdir(basePath)
os.chdir(basePath) # Set working directory to base of notes directory

# Start the CLI if this is the main process
if __name__ == '__main__':
	NoteShell().cmdloop()

