import os

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
						results.append([entry.name, self._ls(path+"/"+entry.name)])
					elif entry.is_file():
						results.append(entry.name)
		return results

	def modifyTime(self, path):
		return os.path.getmtime(path)

	def ls(self):
		dirlist = self._ls('.')
		print(dirlist)
		return dirlist


	def cat(self, path):
		try:
			fileDescriptor = open(path, "r")
			text = fileDescriptor.read()
			return text
		except:
			print("Permission Error")