#! /usr/bin/python3
# CLI Driver for note CLI

import cmd, sys, os, shutil, re
from colorama import init, Fore, Back, Style
init()

basePath = os.path.expanduser("~/.notes")
flatNotesPath = os.path.expanduser("~/.notes/.flat_notes")
textEditorCMD = "subl"
promptColor = Fore.CYAN + Style.BRIGHT

def invalid(reason=""):
	print("Invalid Command.")
	if reason != "":
		print(reason)

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
		cwd = os.getcwd();
		os.chdir(basePath) # Go to root directory
		self.do_git("init") # initialize a git repository
		os.chdir(cwd) # change back to the previous directory


	# Directory to open in text editor
	def do_edit(seld, args):
		'Opens the specified file or directory in sublime text'
		arglist = args.split(" ")
		arglist.insert(0, textEditorCMD)
		pid = os.spawnvp(os.P_NOWAIT, textEditorCMD, arglist)

	def do_ls(self, args):
		'List contents of current directory'
		arglist = args.split(" ")
		firstArg = arglist[0].lower()

		try:
			if firstArg != "":
				if firstArg == "-a" or firstArg == "--all":
					arr = os.scandir(flatNotesPath)
				else:
					arr = os.scandir(args)
			else: 
				arr = os.scandir(".")

			for entry in arr:
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

	def _cat_helper(self, args):
		try:
			fd = open(args, "r")
			text = fd.read()
			fd.close()
			return text
		except: 
			invalid("Cannot cat, check that file exists and that you have read permission.")
			return ""

	def do_cd(self, arg):
		'Navigate within stored notes'
		try:
			os.chdir(arg)
			promptPath = os.getcwd().split('.notes',1)
			# print(promptPath)
			self.promptPath = promptPath[1] if isinstance(promptPath, list) and len(promptPath) > 1 else "/"
		except:
			invalid()

	def do_create(self, args):
		'''
		Command for creating new filters or notes.
		To create a filter - create filter <filter_path>
		To create a note - create note <note_path>
		'''
		arglist = args.split(" ")

		if arglist and len(arglist) >= 2:
			firstArg = arglist[0].lower()
			if firstArg == '-f' or firstArg == '--filter':
				# Create the new filters
				for f in arglist[1:]:
					try:
						os.mkdir(f)
					except:
						print("Filter Already Exists.")
			elif firstArg == '-n' or firstArg == '--note':
				# Create the new notes
				for n in arglist[1:]:
					fd = open(flatNotesPath + '/' + n,"a+")
					fd.write("\n")
					fd.close()
					try:
						os.link(flatNotesPath + '/' + n, n)
					except: 
						print("Note Already Exists.")
			else:
				invalid("Unspecified Creation Type.")

	def do_remove(self, args):
		'''
		Remove all files matching given paths from the current filter
		-r flag allows recursive removal of directories matched
		-p flag allows permanant removal of a note, remove all instances of the note within the notes directory
		'''
		arglist = args.split(" ")
		i, recursive = 0, False
		firstArg = arglist[0].lower()

		if firstArg == "-r" or firstArg == "--remove":
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


	def do_add(self, args):
		'''
		Add an existing notes by NAME not by path to target filter
		add p <path to add to> [ list of files ]
		add [ list of files ] 	--> (added to .)
		'''
		arglist = args.split(" ")
		firstArg = arglist[0].lower()
	
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

	def _add_helper(self, arglist):
		'''
		Should only be called by do_add 
		'''
		for file in arglist:
			os.link(flatNotesPath + "/" + file, './' + file)

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
		arglist = args.split(" ")
		arglist.insert(0, "git")
		pid = os.spawnvp(os.P_NOWAIT, "git", arglist)

		# List of things to render in the UI
	def do_render(self, args):
		'Render target files in the Angular UI'
		arglist = args.split(" ")
		pid = os.spawnvp(os.P_NOWAIT, "", arglist)

	def do_build(self, args):
		'Preprocess notes and send them to the build directory'

	def do_search(self, args):
		'''
		Search for notes. 
		Use the -d flag for a deep search including the bodies of each file
		search [-d] pattern [dir to search in]
		'''
		arglist = args.split(" ")
		firstArg = arglist[0].lower()
		if (firstArg == "-d" or firstArg == "--deep") and len(arglist) >=3:
			# Start the Deep search process
			pattern = arglist[1]
			searchFiles = arglist[2:]
			
			for path in searchFiles:
				path = os.path.expanduser(path)
				if os.path.isdir(path):
					print(self.search_dir(pattern, os.scandir(path)))
				else:
					print(search_file(pattern, path))

		elif len(arglist) >= 1:
			# Just run a quick file name search
			notes = os.listdir(flatNotesPath)
			pattern = arglist[0]

			for note in notes:
				if re.search(pattern, note, re.IGNORECASE):
					print(note)
		else: 
			invalid("Incorrect Number of arguments")

	def search_file(self, pattern, path):
		fd = open(path, "r")
		text = fd.read()
		fd.close()
		return len(re.findall(pattern, text, re.IGNORECASE))

	def search_dir(self, pattern, filelist):
		results = []
		for file in filelist:
			if os.path.isdir(file.path):
				if not file.name.startswith("."): 
					results += self.search_dir(pattern, os.scandir(file.path))
			else:
				results += self.search_file(pattern, file.path);
		return results




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

	# ---------------- OVERRIDES ---------------

	def postcmd(self, stop, line):
		self.prompt = self.promptBase + self.promptPath + self.propmptTerminator


if not os.path.isdir(basePath):
	os.mkdir(basePath)
os.chdir(basePath) # Set working directory to base of notes directory

# Start the CLI if this is the main process
if __name__ == '__main__':
	NoteShell().cmdloop()

# NOTE: When spawning processes, argv[0] MUST be the program name / essentially it gets ignored