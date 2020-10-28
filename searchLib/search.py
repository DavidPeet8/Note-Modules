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
	if not os.path.isdir(basePath):
		return
	try:
		_perf_search(basePath, pattern, isDeep, resultsMap)
	except:
		try:
			_perf_search(basePath, re.escape(pattern), isDeep, resultsMap)
		except:
	 		print("Invalid Regex")

def _perf_search(basePath, pattern, isDeep, resultsMap):
	for file in os.scandir(basePath):
		if file.is_dir():
			_search(file.path, pattern, isDeep, resultsMap)
		elif re.search(pattern, file.name):
			resultsMap[file.name] = resultsMap[file.name] + 1 if file.name in resultsMap else 1

		if isDeep and file.is_file():
			fcontents = open(file.path, 'r', encoding='utf8').read()
			matches = len(re.findall(pattern, fcontents, re.IGNORECASE))
			if matches > 0:
				resultsMap[file.name] = resultsMap[file.name] + matches if (file.name in resultsMap) else matches

def dumpMap(themap, delim=" "):
	for key, value in themap.items():
		print(key, delim, value)