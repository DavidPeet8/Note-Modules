#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import os, atexit
import sys, getopt
import time

hostName = "localhost"
port = 8000
servePath = os.path.expanduser("~/.notes/")
webServer = None

class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

def stopServer():
	print ("Closing HTTP Server on port: " + str(port))
	webServer.server_close()

def main(argv):
	opts, args = getopt.getopt(argv, "hp:d:", ["port=", "dir="]);

	for opt, arg in opts:
		if opt == "-h":
			print ("Options:")
			print ("h - Print semi-helpful things :)")
			print ("-p | --port=<num> - Select the port you wish to serve on")
			print ("-d | --dir=<path> - Select the directory to serve, default is working directory")
		if opt in ("-p", "--port"):
			global port
			port = int(arg)
			print ("Set port: " + arg)
		elif opt in ("-d", "dir="):
			global servePath 
			servePath = os.path.expanduser(string(arg))
			print("Set serve path: " + arg)

	if not os.path.exists(servePath):
		os.makedirs(servePath)
	
	os.chdir(servePath)
	global webServer
	webServer = HTTPServer((hostName, port), RequestHandler)
	print("Serving at port", port)
	atexit.register(stopServer)
	webServer.serve_forever()

main(sys.argv)


