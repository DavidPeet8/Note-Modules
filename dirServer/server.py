#!/usr/bin/python3

from http.server import HTTPServer
import os, atexit, time
import sys, getopt
from config import config, Config
from workingDir import WorkingDir
from requestHandler import RequestHandler



def stopServer():
	print ("Closing HTTP Server on port: " + str(config.port))
	config.webServer.server_close()

def printHelp():
	print ("Options:")
	print ("h - Print semi-helpful things :)")
	print ("-p | --port=<num> - Select the port you wish to serve on")
	print ("-d | --dir=<path> - Select the directory to serve, default is working directory")

def main(argv):
	opts, args = getopt.getopt(argv, "hp:d:", ["port=", "dir="]);

	for opt, arg in opts:
		if opt == "-h":
			printHelp()
		if opt in ("-p", "--port"):
			config.port = int(arg)
			print ("Set port: " + arg)
		elif opt in ("-d", "dir="):
			config.serveDir = os.path.expanduser(string(arg))
			print("Set serve path: " + arg)

	config.currentDir.cd(config.serveDir)
	
	config.webServer = HTTPServer((config.hostName, config.port), RequestHandler)
	print("Serving at port", config.port)
	atexit.register(stopServer)
	config.webServer.serve_forever()

main(sys.argv)


# REturn file last odified tiem along with file data