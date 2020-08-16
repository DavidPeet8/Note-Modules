import { Component, OnInit, Input } from '@angular/core';

@Component({
	selector: 'app-directory-tree',
	templateUrl: './directory-tree.component.html',
	styleUrls: ['./directory-tree.component.sass']
})
export class DirectoryTreeComponent implements OnInit 
{
	@Input() children;
	fileName = "File name";
	isDirectory;
	isOpen = false;
	iconClasses = "fas fa-folder";
	dropdownClasses = "hidden";

	constructor() { }

	ngOnInit(): void 
	{
		this.updateFileIcons();
	}

	updateFileIcons(): void
	{
		if (this.children == undefined || !(this.children instanceof Array))
		{
			this.isDirectory = false;
			this.iconClasses = "fas fa-file";
		} 
		else 
		{
			this.isDirectory = true;
		}
	}

	onClick(): void
	{
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
