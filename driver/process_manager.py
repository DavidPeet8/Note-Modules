import subprocess, webbrowser
import atexit, signal, os


arPID = []

# reap all children onexit
def reap():
	for pid in arPID:
		os.kill(pid, signal.SIGKILL)

atexit.register(reap)

def reap_pid(arpid):
	global arPID
	arPID += arpid

def spawn_quiet(arglist):
	return subprocess.Popen(arglist, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).pid

def spawn(arglist):
	return subprocess.Popen(arglist).pid

def open_default(path):
	webbrowser.open(path)

def run(arglist):
	subprocess.run(arglist)

def spawn_attach_stdout(arglist):
	return subprocess.Popen(arglist, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL);

def spawn_attach_stderr(arglist):
	return subprocess.Popen(arglist, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE);

def spawn_attach_streams(arglist):
	return subprocess.Popen(arglist, stdout=subprocess.PIPE, stderr=subprocess.PIPE);