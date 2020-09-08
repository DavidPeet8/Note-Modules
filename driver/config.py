import os

basePath = os.path.expanduser("~/.notes")
flatNotesPath = basePath + "/.flat_notes"
exePath = os.path.expanduser('~/.notes_cfg')

textEditorCMD = "subl"

PREPROCESSOR_EXE = exePath + "/.exe/preprocessor"
SERVER_EXE = exePath + "/.exe/dirServer/server.py"
UI_EXE = exePath + "/.exe/UI"
RENDER_PORT = "4300"

def update_base_path(path):
	global basePath
	global flatNotesPath
	basePath = os.path.expanduser(path)
	flatNotesPath = basePath + "/.flat_notes"

def print_base_path():
	print("BasePath: " + basePath)

def get_base_path():
	print(basePath)
	return basePath

def get_flat_notes_path():
	return flatNotesPath