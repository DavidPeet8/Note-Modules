from workingDir import WorkingDir
import os

class HTTPServer: pass

class Config:
	hostName = "localhost"
	port = 8000
	serveDir = os.path.expanduser("~/.notes/")
	currentDir = WorkingDir()

config = Config()