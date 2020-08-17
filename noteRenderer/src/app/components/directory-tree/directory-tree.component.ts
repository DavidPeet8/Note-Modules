import { Component, OnInit, Input } from '@angular/core';
import { FileAccessAPIService } from '@services/file-access-api.service';

@Component({
	selector: 'app-directory-tree',
	templateUrl: './directory-tree.component.html',
	styleUrls: ['./directory-tree.component.sass']
})
export class DirectoryTreeComponent implements OnInit 
{
	@Input() basePath;
	@Input() fileDescriptor;
	contentlist = [];
	fileName = "File";
	isDirectory;
	isOpen = false;
	iconClasses = "fas fa-folder";
	dropdownClasses = "hidden";

	constructor(private fileAPI: FileAccessAPIService) { }

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
			this.fileAPI.switchActiveFile(this.basePath + "/" + this.fileName);
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

