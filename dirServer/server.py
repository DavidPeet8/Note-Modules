#!/usr/bin/python3

from http.server import HTTPServer
import os, atexit, time
import sys, argparse
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


def get_server_args(arglist):
	parser = argparse.ArgumentParser()
	parser.add_argument('-h', '--help', action="store_true")
	parser.add_argument('-p', '--port', type=int)
	parser.add_argument('-d', '--dir')

def main(argv):
	args = get_server_args(argv)
	opts, args = getopt.getopt(argv, "hp:d:", ["port=", "dir="]);

	if args.help:
		printHelp()
		return
	if args.port:
		config.port = args.port
		print ("Set port: " + args.port)
	elif args.dir:
		config.serveDir = os.path.expanduser(args.dir)
		print("Set serve path: " + args.dir)

	config.currentDir.cd(config.serveDir)
	
	config.webServer = HTTPServer((config.hostName, config.port), RequestHandler)
	print("Serving at port", config.port)
	atexit.register(stopServer)
	config.webServer.serve_forever()

main(sys.argv)


# REturn file last odified tiem along with file data