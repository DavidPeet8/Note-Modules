#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import os, atexit, time
import sys, getopt
import json

hostName = "localhost"
port = 8000
webServer = None
serveDir = os.path.expanduser("~/.notes/")
currentDir = None

class WorkingDir:
	servePath = ""
	def cd(self, path):
		if not os.path.exists(path):
			os.makedirs(path)

		os.chdir(path)
		self.serveDir = path

	def _ls(self, path):
		results = [];
		with os.scandir(path) as it:
			for entry in it:
				if  not entry.name.startswith('.'): 
					if entry.is_dir():
						print(entry)
						results.append([entry.name, self._ls(path+"/"+entry.name)])
					elif entry.is_file():
						results.append(entry.name)
		return results

	def ls(self):
		dirlist = self._ls('.')
		print(dirlist)
		return dirlist


	def cat(self, fileName):
		if fileName in self.ls():
			try:
				fileDescriptor = open(fileName, "rb")
				text = fileDescriptor.read()
				return text
			except:
				print("Permission Error")


class RequestHandler(BaseHTTPRequestHandler):
	
	def setAccessControlHeaders(self):
		self.send_header("Access-Control-Allow-Origin", "*")
		self.send_header("Access-Control-Allow-Methods", "GET")
		self.send_header("Access-Control-Allow-Headers", "*")
		self.send_header("Access-Control-Expose-Headers", "*")
		self.send_header("Access-Control-Allow-Credentials", "true")

	def do_HEAD(self):
		self.send_response(200)
		self.setAccessControlHeaders()
		self.end_headers()

	def do_GET(self):
		encodedJson = ""
		responseStatus = 200;
		
		if (self.path == "/file-list"):
			contents = currentDir.ls()
			print(contents)
			encodedJson = json.dumps({'dirs': contents}).encode()
		elif (self.path[1:] in currentDir.ls()):
			encodedJson = currentDir.cat(self.path[1:])
		else: 
			# prefix with b so it is treated as a bytestring not a string obj
			encodedJson = "Cannot find requested file"
			responseStatus = 404

		self.send_response(responseStatus)
		self.send_header("Content-type", "text/json")
		self.setAccessControlHeaders();
		self.end_headers()
		self.wfile.write(encodedJson) # .encode() to treat as bytestring not obj


def stopServer():
	print ("Closing HTTP Server on port: " + str(port))
	webServer.server_close()

def printHelp():
	print ("Options:")
	print ("h - Print semi-helpful things :)")
	print ("-p | --port=<num> - Select the port you wish to serve on")
	print ("-d | --dir=<path> - Select the directory to serve, default is working directory")

def main(argv):
	global currentDir, port, serveDir, webServer
	currentDir = WorkingDir()
	opts, args = getopt.getopt(argv, "hp:d:", ["port=", "dir="]);

	for opt, arg in opts:
		if opt == "-h":
			printHelp()
		if opt in ("-p", "--port"):
			port = int(arg)
			print ("Set port: " + arg)
		elif opt in ("-d", "dir="):
			serveDir = os.path.expanduser(string(arg))
			print("Set serve path: " + arg)

	currentDir.cd(serveDir)
	
	webServer = HTTPServer((hostName, port), RequestHandler)
	print("Serving at port", port)
	atexit.register(stopServer)
	webServer.serve_forever()

main(sys.argv)


