#!/usr/bin/python3

import os, json, sys

path = os.path.expanduser("~/.notes_cfg/config/config.json")

with open(path, "r") as config:
	data = config.read()

json = json.loads(data)

# ------------------------ ACCESSORS ----------------------------

def get_notes_path():
	return os.path.expanduser(json["notes_cfg"]["base_path"])

def get_flat_notes_path():
	return os.path.expanduser(json["notes_cfg"]["flat_notes_path"])

def get_cfg_path():
	return os.path.expanduser(json["exe_cfg"]["base_path"])

def get_exe_path():
	return os.path.expanduser(json["exe_cfg"]["exe_path"])

def get_render_dbg_port():
	return json["renderer"]["debug"]["port"]

def get_render_dbg_host():
	return json["renderer"]["debug"]["host_name"]

def get_render_host():
	return json["renderer"]["prod"]["host_name"]

def get_dir_server_port():
	return json["dir_server"]["port"]

def get_dir_server_host():
	return json["dir_server"]["host_name"]

def get_default_editor():
	return os.path.expanduser(json["default_apps"]["text_editor_path"])

def get_preproc_path():
	return os.path.expanduser(get_exe_path() + json["processes"]["preprocessor_pathsfx"])

def get_dir_server_path():
	return os.path.expanduser(get_exe_path() + json["processes"]["server_pathsfx"])

def get_ui_path():
	return os.path.expanduser(get_exe_path() + json["processes"]["ui_pathsfx"])

def get_search_path():
	return os.path.expanduser(get_exe_path() + json["processes"]["search_engine_pathsfx"])

def get_git_path():
	return os.path.expanduser(json["external_procs"]["git_path"])

# ------------------------- MUTATORS -------------------------

def update_base_path(path):
	json["notes_cfg"]["base_path"] = os.path.expanduser(path)
	json["notes_cfg"]["flat_notes_path"] = json["notes_cfg"]["base_path"] + "/.flat_notes"