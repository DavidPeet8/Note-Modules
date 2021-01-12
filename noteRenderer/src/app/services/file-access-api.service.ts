import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

class File {
	activeFileURI = "";
	activeFileText = null;
	lastModifiedTime = null;
}

class Dir {
	dirlist: File[] = [];
	lastModifiedTime = null;
}


@Injectable({
	providedIn: 'root'
})
export class FileAccessAPIService {
	rootDir = new Dir();
	activeFile = new File();
	publishDirEvent = null;
	publishCodeEvent = null;
	host = 'http://localhost:8000'; // TODO: change this to being read from a file

	constructor(private router: Router) {
		this._fetchDirList();
		this._fetchFile(this.activeFile.activeFileURI);
		let checkDModified = this._checkDirListModified.bind(this);
		let checkFModified = this._checkFileModified.bind(this);
		setInterval(() => {
			if (!document.hidden) {
				checkDModified();
				checkFModified();
			}
		}, 5000);
	}

	async _fetchDirList() {
		let dirlist;
		await fetch(this.host + "/dirtree")
			.then((data) => {
				return data.json();
			})
			.then((json) => {
				console.log("Rerieved response for dirlist")
				this.rootDir.dirlist = json.dirs;
				this.rootDir.lastModifiedTime = json.modifyTime;
				this.publishDirEvent();
			})
			.catch((err) => {
				this.router.navigate(['install']);
			});
	}

	async _fetchFile(fileName) {
		if (fileName == "") { return; }

		await fetch(this.host + "/note" + fileName)
			.then((data) => {
				return data.json();
			})
			.then((json) => {
				this.activeFile.activeFileText = json.fileData;
				this.activeFile.lastModifiedTime = json.modifyTime;
				this.publishCodeEvent(fileName);
			})
			.catch((e) => {
				this._fetchDirList();
			});
	}

	async _checkFileModified() {
		if (this.activeFile.activeFileURI == "") { return; }

		await fetch(this.host + '/status/note' + this.activeFile.activeFileURI)
			.then((data) => {
				return data.text()
			})
			.then((text) => {
				if (text != this.activeFile.lastModifiedTime) {
					this._fetchFile(this.activeFile.activeFileURI); // File was Modified
				}
			})
			.catch((e) => {
				console.log("Failed to check for active file modifications", e)
			});
	}

	async _checkDirListModified() {
		await fetch(this.host + "/status/dirtree")
			.then((data) => {
				return data.text()
			})
			.then((text) => {
				console.log("Checking Dir List - lastModifiedTime: " + text);
				console.log("Old Last Modified Time: " + this.rootDir.lastModifiedTime);
				if (text != this.rootDir.lastModifiedTime) {
					console.log("different last modified time")
					this._fetchDirList(); // DirTree was Modified
				}
			})
			.catch((e) => {
				console.log("Failed to check for Dir Tree modifications", e)
			});
	}

	// ----------------------------PUBLIC INTERFACE -------------------------------

	getDirList() {
		return this.rootDir.dirlist;
	}

	getCurrentFile(): String {
		return this.activeFile.activeFileText;
	}

	// Switch active file to partialURI and force an immediate fetch
	switchActiveFile(partialURI): void {
		if (partialURI == this.activeFile.activeFileURI) return;
		this.activeFile.activeFileURI = partialURI;
		this._fetchFile(partialURI);
	}

	setPublishMethod(publishMethods): void {
		this.publishDirEvent = publishMethods.dirEvent;
		this.publishCodeEvent = publishMethods.codeEvent;
	}

	async doSearch(searchTerm, isDeep, callback) {
		let queryString = isDeep ? "?deep=true" : "?deep=false";
		await fetch(this.host + "/search/" + searchTerm + queryString, { method: 'POST' })
			.then((data) => {
				return data.json();
			})
			.then((json) => {
				callback(json);
			});
	}
}
