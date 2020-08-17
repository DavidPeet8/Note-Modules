import { Component, OnInit, Input } from '@angular/core';

@Component({
	selector: 'app-directory-tree',
	templateUrl: './directory-tree.component.html',
	styleUrls: ['./directory-tree.component.sass']
})
export class DirectoryTreeComponent implements OnInit 
{
	@Input() fileDescriptor;
	contentlist = [];
	fileName = "File name";
	isDirectory;
	isOpen = false;
	iconClasses = "fas fa-folder";
	dropdownClasses = "hidden";

	constructor() { }

	ngOnInit(): void 
	{
		this.updateFileIcons();
		this.updateFileName();
		this.updateDirList();
	}

	updateDirList(): void 
	{
		if (this.fileDescriptor instanceof Array)
		{
			this.contentlist = this.fileDescriptor[1];
		} 
		else 
		{
			this.contentlist = [];
		}
	}

	updateFileIcons(): void
	{
		if (this.fileDescriptor == undefined || !(this.fileDescriptor instanceof Array))
		{
			this.isDirectory = false;
			this.iconClasses = "fas fa-file";
		} 
		else 
		{
			this.isDirectory = true;
		}
	}

	updateFileName(): void
	{
		this.fileName = (this.fileDescriptor instanceof Array) ? this.fileDescriptor[0] : this.fileDescriptor;
	}

	openFile(): void 
	{

		if (!this.isDirectory)
		{
			console.log("open file: " + this.fileName);
			// Actually open this file in the code thing
		}

		if (this.isDirectory && !this.isOpen) 
		{
			this.iconClasses = "fas fa-folder-open";
			this.isOpen = true;
			this.dropdownClasses = "children-dropdown show";
		}
		else if (this.isDirectory && this.isOpen)
		{
			this.iconClasses = "fas fa-folder";
			this.isOpen = false;
			this.dropdownClasses = "hidden";
		}
	}
}

