#! /usr/bin/python3

import os, subprocess
from shutil import copy, copytree, rmtree

basePath = os.path.expanduser("~/.notes")
installPath = os.path.expanduser("~/.notes/.exe")

if not os.path.exists(basePath):
	os.mkdir(basePath)

if not os.path.exists(installPath):
	os.mkdir(installPath)
else:
	rmtree(installPath)
	print("Cleaned old installation")



print("Necessary Directories Created")


# Install the directory server
copytree("./dirServer", installPath+ "/dirServer")
print("Installed Local Directory Server")
# Remake the file
cwd = os.getcwd()
os.chdir("./preprocessor")
subprocess.run(["make", "debug"])
print("Remade Preprocessor")
os.chdir(cwd)
# Install the preprocessor
copy("./preprocessor/preprocessor", installPath + "/preprocessor")
print("Installed Preprocessor")
# Install the UI
copytree("./noteRenderer/build", installPath + "/UI")
print("Installed UI")
# Install the cli driver
copytree("./driver", installPath + installPath + "/driver")
print("Installed CLI")

copy("./notes_gitignore", basePath + "/.gitignore")
