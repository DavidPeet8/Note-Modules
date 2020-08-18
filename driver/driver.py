#! /usr/bin/python3
# CLI Driver for note CLI

import cmd, sys, os	
from colorama import init, Fore, Back, Style
init()

def fork():
	try:
		pid = os.fork()
	except OSError as e:
		raise RuntimeError("Fork Failed: %s [%d]" % (e.strerror, e.errno))
	return pid

class NoteShell (cmd.Cmd):
	intro = "Welcome to NoteShell.\nAuthor: David Peet\nGithub: davidpeet8\nType help or ? for a list of commands.\n"
	promptBase = Fore.CYAN + Style.BRIGHT + "(NoteShell) " 
	promptPath = ""
	propmptTerminator = ": " + Style.RESET_ALL
	prompt = Fore.CYAN + Style.BRIGHT + "(NoteShell) : " + Style.RESET_ALL

	# should recieve no arguments
	def do_init(self, arg):
		'Initialize directories needed for this application to function as required'
		os.mkdir("~/.notes")
		os.mkdir("~/.notes/.flat_notes")
		os.mkdir("~/.notes/build")

	# Directory to open in text editor
	def do_edit(seld, args):
		'Opens the specified file or directory in sublime text'
		arglist = args.split(" ")
		print(arglist)
		pid = os.fork()

		if pid == 0: # Child Process
			os.execvp("subl", arglist)

	# List of things to render in the UI
	def do_render(self, args):
		arglist = args.split(" ")
		pid = os.fork()

		if pid == 0:
			os.execlp() # Start Angular UI

	def do_ls(self, args):
		'List contents of current directory'
		if isinstance(args, list):
			arr = os.scandir(args[0])
		elif args != "":
			arr = os.scandir(args)
		else: 
			arr = os.scandir(".")

		for entry in arr:
			if entry.is_dir():
				print(Fore.BLUE + Style.BRIGHT + entry.name)
				print(Style.RESET_ALL, end="")
			else:
				print(entry.name)

	def do_cat(self, args):
		'Print out the contents of the argument file'
		try:
			fd = open(args, "r")
			text = fd.read()
			fd.close()
			print(text)
		except: 
			print("Cannot cat, check that file exists and that you have read permission.")

	def do_cd(self, arg):
		'Navigate within stored notes'
		try:
			os.chdir(arg)
			promptPath = os.getcwd().split('.notes',1)
			# print(promptPath)
			self.promptPath = promptPath[1] if isinstance(promptPath, list) and len(promptPath) > 1 else "/"
		except:
			return

	def do_create(self, args):
		'Command for creating new filters or notes.\nTo create a filter - create filter <filter_path>\nTo create a note - create note <note_path>'
		arglist = args.split(" ")
		print(arglist[1:])
		if arglist and len(arglist) >= 2:
			low = arglist[0].lower()
			if low == 'f' or low == 'filter':
				# Create the new filters
				for f in arglist[1:]:
					os.mkdir(f)
			elif low == 'n' or low == 'note':
				# Create the new notes
				for n in arglist[1:]:
					fd = open(n,"a+")
					fd.write("\n")
					fd.close()
			else:
				print("Unspecified type to create")

	def do_build(self, args):
		'Preprocess notes and send them to the build directory'

	def do_quit(self, args):
		'Quit the command line interface'
		sys.exit()

	# -------------------- ALIASES -------------------

	def do_c(self, args):
		'Alias for Create command'
		self.do_create(args) 

	def do_b(self, args):
		'Alias for build command'
		self.do_build(args);

	def do_q(self, args):
		'Alias for quit'
		self.do_quit(args)

	# ---------------- OVERRIDES ---------------

	def postcmd(self, stop, line):
		self.prompt = self.promptBase + self.promptPath + self.propmptTerminator



os.chdir(os.path.expanduser("~/.notes")) # Set working directory to base of notes directory

# Start the CLI if this is the main process
if __name__ == '__main__':
	NoteShell().cmdloop()