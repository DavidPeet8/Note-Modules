import argparse

def get_driver_args(arglist):
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--path', help="Path to open as the base directory for note modules CLI")
	return parser.parse_args(arglist)

def get_edit_args(arglist):
	parser = argparse.ArgumentParser()
	parser.add_argument('-c', '--command', help="custom command to open the file Ex subl for sublime text")
	parser.add_argument('paths', nargs='+')
	return parser.parse_args(arglist)

def get_create_args(arglist):
	parser = argparse.ArgumentParser()
	parser.add_argument('-f', '--filter', nargs="+", help="Indicate to create filters")
	parser.add_argument('-n', '--note', nargs="+", help='Indicate to create a note')
	return parser.parse_args(arglist)

def get_ls_args(arglist):
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--notes', action="store_true", help="List all notes in flat_notes")
	parser.add_argument('-a', '--all', action="store_true", help="List all files including hidden ones")
	parser.add_argument('path', nargs="?", help="Path to list", default=".")
	return parser.parse_args(arglist)

def get_remove_args(arglist):
	parser = argparse.ArgumentParser()
	parser.add_argument('-r', '--recursive', action="store_true", help="Recursively remove a directory")
	parser.add_argument('-p', '--permanent', action="store_true", help="Remove all instances of target")
	parser.add_argument('paths', nargs="+", help="Targets to remove")
	return  parser.parse_args(arglist)

def get_add_args(arglist):
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', '--path', help="Specifies the path to add to")
	parser.add_argument('targets', nargs="+")
	return parser.parse_args(arglist)


def get_search_args(arglist, default_files_path):
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--deep', action='store_true', help="Search the contents of files instead of their names")
	parser.add_argument('pattern', help="Pattern to search for")
	parser.add_argument('files', nargs="*", default=default_files_path)
	return parser.parse_args(arglist)

def get_render_args(arglist):
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--debug', action='store_true', help="Enter debug mode and host UI on localhost")
	parser.add_argument('-a', '--attach', action='store_true', help="Only launch dir server, not UI")
	parser.add_argument('-v', '--view', action="store_true", help="launch the UI")
	parser.add_argument('target', nargs="?")
	return parser.parse_args(arglist)

