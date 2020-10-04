from workingDir import WorkingDir
import os, sys

sys.path.insert(1, os.path.expanduser("~/.notes_cfg/exe/configLib"))
from config_reader import *

# class HTTPServer: pass

class Config:
	hostName = get_dir_server_host()
	port = get_dir_server_port()
	serveDir = os.path.expanduser(get_notes_path())
	currentDir = WorkingDir()

config = Config()