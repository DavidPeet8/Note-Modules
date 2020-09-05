import os

basePath = os.path.expanduser("~/.notes")
flatNotesPath = basePath + "/.flat_notes"

textEditorCMD = "subl"

PREPROCESSOR_EXE = basePath + "/.exe/preprocessor"
SERVER_EXE = basePath + "/.exe/dirServer/server.py"
UI_EXE = basePath + "/.exe/UI"
RENDER_PORT = "4300"

def update_base_path(path):
	global basePath
	global flatNotesPath
	basePath = os.path.expanduser(path)
	flatNotesPath = basePath + "/.flat_notes"

def print_base_path():
	print("BasePath: " + basePath)

def get_base_path():
	return basePath

def get_flat_notes_path():
	return flatNotesPath