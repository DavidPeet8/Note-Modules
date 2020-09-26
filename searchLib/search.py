# /usr/bin/python3

import os, re

def searchDirList(basePaths, pattern, isDeep):
	resultsMap = {}
	for path in basePaths:
		_search(os.path.expanduser(path), pattern, isDeep, resultsMap)

	return resultsMap

def searchDir(basePath, pattern, isDeep):
	resultsMap = {}
	_search(os.path.expanduser(basePath), pattern, isDeep, resultsMap)
	return resultsMap

def _search(basePath, pattern, isDeep, resultsMap):
	for file in os.scandir(basePath):
		if file.is_dir():
			_search(file.path, pattern, isDeep, resultsMap)
		elif re.match(pattern, file.name):
			resultsMap[file.name] = 1

		if isDeep and file.is_file():
			fcontents = open(file.path, 'r', encoding='utf8').read()
			matches = len(re.findall(pattern, fcontents))
			if matches > 0:
				if not file.name in resultsMap:
					resultsMap[file.name] = matches
				else: 
					resultsMap[file.name] += matches

def dumpMap(themap, delim=" "):
	for key, value in themap.items():
		print(key, delim, value)