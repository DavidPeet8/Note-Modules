import { Injectable } from '@angular/core';

class File 
{
	activeFileURI = "";
	activeFileText = null;
	lastModifiedTime = null;
}

class Dir 
{
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
	host = 'http://localhost:8000';

	constructor() 
	{ 
		this._fetchDirList();
		this._fetchFile(this.activeFile.activeFileURI);
		setInterval(() => {
			this._checkDirListModified.bind(this)();
			this._checkFileModified.bind(this)();
		}, 5000);
	}

	async _fetchDirList()
	{
		let dirlist;
		await fetch(this.host + this._getQueryParams({modify: false})).then((data) => { 
			return data.json();
		}).then((json) => {
			this.rootDir.dirlist = json.dirs;
			this.rootDir.lastModifiedTime = json.modifyTime;
			this.publishDirEvent();
		});
	}

	async _fetchFile(fileName)
	{
		await fetch(this.host + '/' + this.activeFile.activeFileURI + this._getQueryParams({modify: false})).then((data) => {
			return data.json();
		}).then((json) => {
			this.activeFile.activeFileText = json.fileData;
			this.activeFile.lastModifiedTime = json.modifyTime;
			this.publishCodeEvent(this.activeFile.activeFileURI);
		});
	}

	async _checkFileModified()
	{
		await fetch(this.host + '/' + this.activeFile.activeFileURI + this._getQueryParams({modify: true})).then((data) => {
			return data.text()
		}).then((text) => {
			if (text != this.activeFile.lastModifiedTime) 
			{
				this._fetchFile(this.activeFile.activeFileURI); // File was Modified
			}
		});
	}

	async _checkDirListModified()
	{
		await fetch(this.host + this._getQueryParams({modify: true})).then((data) => {
			return data.text()
		}).then((text) => {
			if (text != this.rootDir.lastModifiedTime) 
			{
				this._fetchDirList(); // DirTree was Modified
			}
		});
	}

	_getQueryParams(data): String
	{
		return '?modify='+ data.modify;
	}


	// ----------------------------PUBLIC INTERFACE -------------------------------

	getDirList()
	{
		return this.rootDir.dirlist;
	}

	getCurrentFile(): String 
	{
		return this.activeFile.activeFileText;
	}

	// Switch active file to partialURI and force an immediate fetch
	switchActiveFile(partialURI): void
	{
		if(partialURI == this.activeFile.activeFileURI) return;
		this.activeFile.activeFileURI = partialURI;
		this._fetchFile(partialURI);
	}

	setPublishMethod(publishMethods): void
	{
		this.publishDirEvent = publishMethods.dirEvent;
		this.publishCodeEvent = publishMethods.codeEvent;
	}
}
