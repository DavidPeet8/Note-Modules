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
subprocess.run(["make"])
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
