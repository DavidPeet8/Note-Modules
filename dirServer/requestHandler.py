from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import re

from config import config, Config

def pathExistsInCurrentDir(path):
	pathArr = re.split('/', path)
	currArr = config.currentDir.ls()

	for i in range(len(pathArr)):
		matched = False
		for j in range(len(currArr)):
			if isinstance(currArr[j], list) and pathArr[i] == currArr[j][0]:
				matched = True
				currArr = currArr[j][1] 
				break;
		if i == len(pathArr)-1 and pathArr[i] == currArr[j]:
				return True
		elif matched == False: 
			return False

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
		url = urlparse(self.path)
		print(url.query)
		if url.query == 'modify=true':
			# We are looking for modification times not actual data
			# Exists to reduce polling payload size
			encodedJson = str(config.currentDir.modifyTime('.' + url.path)).encode()

		elif (url.path == "/"):
			contents = config.currentDir.ls()
			encodedJson = json.dumps({
				'dirs': contents,
				'modifyTime': config.currentDir.modifyTime(".")
			}).encode()
		elif pathExistsInCurrentDir(url.path[1:]):
			encodedJson = json.dumps({
				'fileData': config.currentDir.cat(url.path[1:]), 
				'modifyTime': config.currentDir.modifyTime(url.path[1:])
			}).encode();
		else: 
			# prefix with b so it is treated as a bytestring not a string obj
			encodedJson = b"Cannot find requested file"
			responseStatus = 404

		self.send_response(responseStatus)
		self.send_header("Content-type", "text/json")
		self.setAccessControlHeaders();
		self.end_headers()
		self.wfile.write(encodedJson) # .encode() to treat as bytestring not obj