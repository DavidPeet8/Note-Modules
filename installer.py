#! /usr/bin/python3

import os, subprocess
from shutil import copy, copytree, rmtree
import sys, getopt
# getopt is a bit simpler than arg parse even though it is not the recommended module

basePath = os.path.expanduser("~/.notes")
installPath = os.path.expanduser("~/.notes/.exe")
notesDirPaths = [os.path.expanduser("~/.notes")]

if not os.path.exists(basePath):
	os.mkdir(basePath)

if not os.path.exists(installPath):
	os.mkdir(installPath)
else:
	rmtree(installPath)
	print("Cleaned old installation")
try:
	opts, args = getopt.getopt(sys.argv[1:], "p:", ["path="])
except getopt.GetoptError:
	print("Failed to get options, Exiting.")
	sys.exit(1)

for opt, arg in opts:
	if opt in ('-p', '--path'):
		newPath = os.path.expanduser(arg)
		notesDirPaths += [newPath]

		if not os.path.exists(newPath):
			os.mkdir(newPath)

print("Necessary Directories Created")


# Install the directory server
copytree("./dirServer", installPath + "/dirServer")
print("Installed Local Directory Server")
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
	copy("./notes_gitignore", path + "/.gitignore")
