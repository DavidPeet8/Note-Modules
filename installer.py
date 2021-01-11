#! /usr/bin/python3

import os, subprocess
from shutil import copy, copytree, rmtree
import sys, argparse

basePath = os.path.expanduser("~/.notes_cfg")
installPath = os.path.expanduser("~/.notes_cfg/exe")
notesDirPath = os.path.expanduser("~/.notes")
cfgPath = basePath + "/config"

def parse_args(arglist):
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--path')
	parser.add_argument('-d', '--debug', action="store_true")
	parser.add_argument('-c', '--clean', action="store_true")
	parser.add_argument('-l', '--loglevel', default=-1) # Store -1 so we make a prod build
	return parser.parse_args(arglist)

args = parse_args(sys.argv[1:])
call_path = os.path.dirname(os.path.abspath(sys.argv[0]));

if args.path:
	notesDirPath = os.path.expanduser(args.path)

# Create main and subdirectories if needed
if not os.path.exists(notesDirPath):
	os.mkdir(notesDirPath)
if not os.path.exists(notesDirPath + "/.flat_notes"):
	os.mkdir(notesDirPath + "/.flat_notes")

if not os.path.exists(basePath):
	os.mkdir(basePath)

if not os.path.exists(installPath):
	os.mkdir(installPath)
else:
	rmtree(installPath)
	print("Cleaned old installation")

if not os.path.exists(cfgPath):
	os.mkdir(cfgPath)
else:
	rmtree(cfgPath)
	print("Cleaned old configuration")

print("Necessary Directories Created")

# ---------------------------------------------------------------------------------------------

# Install the directory server
copytree(call_path + "/dirServer", installPath + "/dirServer")
print("Installed Local Directory Server")

# Install the search library
copytree(call_path + "/searchLib", installPath + "/searchLib")
print("Installed python searching library")

# Install the config library
copytree(call_path + "/configLib", installPath + "/configLib")
print("Installed python configuration library")

# Install config files
copytree(call_path + "/config", cfgPath)
print("Installed configuration files")

# Remake the file
cwd = os.getcwd()
os.chdir(call_path + "/preprocessor")
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
copy(call_path + "/preprocessor/preprocessor", installPath + "/preprocessor")
print("Installed Preprocessor")

# Install the UI
copytree(call_path + "/noteRenderer/build", installPath + "/UI")
print("Installed UI")

# Install the cli driver
copytree(call_path + "/driver", installPath + "/driver")
os.rename(installPath + "/driver/driver.py", installPath + "/driver/notes")
print("Installed CLI")

# Install the gitignore
copy(call_path + "/notes_gitignore", notesDirPath + "/.gitignore")
