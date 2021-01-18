#!/usr/bin/python3

import os
import sys, argparse
from config import config
from requestHandler import start_rest_api


def printHelp():
	print ("Options:")
	print ("h - Print semi-helpful things :)")
	print ("-p | --port=<num> - Select the port you wish to serve on")
	print ("-d | --dir=<path> - Select the directory to serve, default is working directory")


def get_server_args(arglist):
	parser = argparse.ArgumentParser(add_help=False)
	parser.add_argument('-h', '--help', action='store_true')
	parser.add_argument('-p', '--port', type=int)
	parser.add_argument('-d', '--dir')
	return parser.parse_args(arglist)

def main(argv):
	args = get_server_args(argv)

	if args.help:
		printHelp()
		return
	if args.port:
		config.port = args.port
		print ("Set port: " + str(args.port))
	if args.dir:
		config.serveDir = os.path.expanduser(args.dir)
		print("Set serve path: " + args.dir)

	config.currentDir.cd(config.serveDir)
	start_rest_api(config.hostName, config.port)

main(sys.argv[1:])
