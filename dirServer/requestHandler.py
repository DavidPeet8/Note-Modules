from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json, re, sys, os
from flask import Flask, request, jsonify, send_file, Response

from config import config, Config

sys.path.insert(1, os.path.expanduser("~/.notes_cfg/.exe/searchLib"))
from search import searchDir, dumpMap

app = Flask(__name__)

def pathExistsInCurrentDir(pathArr):
	currArr = config.currentDir.ls_all()

	for i in range(len(pathArr)):
		matched = False
		for j in range(len(currArr)):
			if isinstance(currArr[j], list) and pathArr[i] == currArr[j][0]:
				# print("Matched "+ pathArr[i] + " with " + currArr[j][0])
				matched = True
				currArr = currArr[j][1] 
				break;
			if i == len(pathArr) - 1 and pathArr[i] == currArr[j]:
				return True
		if matched == False: 
			return False

	
def setAccessControlHeaders(resp):
	resp.headers["Access-Control-Allow-Origin"] = "*"
	resp.headers["Access-Control-Allow-Methods"] = "GET"
	resp.headers["Access-Control-Allow-Headers"] = "*"
	resp.headers["Access-Control-Expose-Headers"] = "*"
	resp.headers["Access-Control-Allow-Credentials"] = "true"
	return resp


def start_rest_api(_host, _port):
	app.run(host=_host, port=_port, debug=False)


def start_rest_api_for_debug(host, port):
	app.run(debug=True, host=_host, port=_port)

@app.route('/note/', defaults={'note_path': ''})
@app.route('/note/<path:note_path>', methods=['GET'])
def get_note(note_path):
	url = re.split('/', note_path)

	if pathExistsInCurrentDir(url):
		resp = jsonify({
			'fileData': config.currentDir.cat(note_path), 
			'modifyTime': config.currentDir.modifyTime(note_path)
		})

		return setAccessControlHeaders(resp)


@app.route('/status/note/<path:note_path>', methods=['GET'])
def get_note_updates(note_path):
	resp = Response(str(config.currentDir.modifyTime('./' + note_path)))
	return setAccessControlHeaders(resp)


@app.route('/dirtree', methods=['GET'])
def get_dir_tree():
	basePathForRequest = './'
	contents = config.currentDir.ls()
	resp = jsonify({
		'dirs': contents,
		'modifyTime': config.currentDir.modifyTime(basePathForRequest)
	})
	return setAccessControlHeaders(resp)


@app.route('/status/dirtree', methods=['GET'])
def get_dir_tree_updates():
	resp = Response(str(config.currentDir.modifyTime(config.serveDir)))
	return setAccessControlHeaders(resp)

@app.route('/image/<string:image_name>', methods=['GET'])
def get_image(image_name):
	basePathForRequest = config.serveDir + '.assets/'
	resp = send_file(basePathForRequest + image_name, mimetype='image/gif')
	return setAccessControlHeaders(resp)

@app.route('/search/<string:search_term>', methods=['POST'])
def do_search(search_term):
	isDeep = request.args.get('deep').lower() == "true";
	fileMap = searchDir("~/.notes/.flat_notes", search_term, isDeep)

	resp = jsonify(fileMap)
	return setAccessControlHeaders(resp)