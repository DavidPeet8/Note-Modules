#! /usr/bin/python3

import os, subprocess
from shutil import copy, copytree, rmtree
import sys, argparse
# getopt is a bit simpler than arg parse even though it is not the recommended module

basePath = os.path.expanduser("~/.notes_cfg")
installPath = os.path.expanduser("~/.notes_cfg/.exe")
notesDirPaths = [os.path.expanduser("~/.notes")]

def parse_args(arglist):
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--path')
	parser.add_argument('-d', '--debug', action="store_true")
	parser.add_argument('-c', '--clean', action="store_true")
	parser.add_argument('-l', '--loglevel')
	parser.add_argument('--prod', action="store_true")
	return parser.parse_args(arglist)

if not os.path.exists(basePath):
	os.mkdir(basePath)

if not os.path.exists(installPath):
	os.mkdir(installPath)
else:
	rmtree(installPath)
	print("Cleaned old installation")

args = parse_args(sys.argv[1:])

if args.path:
	newPath= os.path.expanduser(args.path)
	notesDirPaths += [newPath]

	if not os.path.exists(newPath):
			os.mkdir(newPath)		


print("Necessary Directories Created")

# Install the directory server
copytree("./dirServer", installPath + "/dirServer")
print("Installed Local Directory Server")
# Install the search library
copytree("./searchLib", installPath + "/searchLib")
print("Installed python searching library")
# Remake the file
cwd = os.getcwd()
os.chdir("./preprocessor")
loglevel = int(args.loglevel)

if args.clean:
	subprocess.run(["make", "clean"])

if args.debug or loglevel >= 4:
	subprocess.run(["make", "debug"])
elif loglevel == 0:
	subprocess.run(["make", "silent"])
elif loglevel == 1:
	subprocess.run(["make", "error"])
elif loglevel == 2:
	subprocess.run(["make", "warn"])
elif loglevel == 3:
	subprocess.run(["make", "info"])
else:
	subprocess.run(["make", "prod"])

print("Remade Preprocessor")
os.chdir(cwd)
# Install the preprocessor
copy("./preprocessor/preprocessor", installPath + "/preprocessor")
print("Installed Preprocessor")
# Install the UI
copytree("./noteRenderer/build", installPath + "/UI")
print("Installed UI")
# Install the cli driver
copytree("./driver", installPath + "/driver")
os.rename(installPath + "/driver/driver.py", installPath + "/driver/notes")
print("Installed CLI")

for path in notesDirPaths:
	if not os.path.exists(path):
		os.mkdir(path)
	copy("./notes_gitignore", path + "/.gitignore")
