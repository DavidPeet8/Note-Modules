import os

# Should be a better implementation of this somewhere
def dir_empty(path):
	return os.listdir(path)

def check_and_mkdir(path):
	if not os.path.isdir(path):
		os.mkdir(path)
	print("Directory exists.")

def check_and_mkdirs(ar_paths):
	for path in ar_paths:
		check_and_mkdir(path)

def temp_chdir_run(path, func, args):
	cwd = os.getcwd();
	os.chdir(path) 
	func(*args)
	os.chdir(cwd)

def temp_chdir_run_list(path, funclist, argslist):
	cwd = os.getcwd()
	os.chdir(path)
	for func, args in zip(funclist, argslist):
		func(*args)
	os.chdir(cwd)

def touch_file(path):
	fd = open(path, "a+")
	fd.write("")
	fd.close()

def dir_contents(path=os.getcwd()):
	dirname = os.path.dirname(path)
	dirname = dirname if dirname else "."
	if os.path.exists(dirname):
		return os.scandir(dirname)

