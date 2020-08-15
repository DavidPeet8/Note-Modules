import { Component, OnInit, Input, ViewChild, ElementRef, AfterViewInit } from '@angular/core';

@Component({
	selector: 'app-directory-tree',
	templateUrl: './directory-tree.component.html',
	styleUrls: ['./directory-tree.component.sass']
})
export class DirectoryTreeComponent implements OnInit, AfterViewInit 
{
	@Input() children;
	@ViewChild("dirSection") dirSection: ElementRef;
	fileName = "File name";
	isDirectory;
	isOpen = false;
	iconClasses = "fas fa-folder";
	dropdownClasses = "hidden";

	constructor() { }

	ngOnInit(): void 
	{
		if (this.children == undefined || this.children.length == 0)
		{
			this.isDirectory = false;
			this.iconClasses = "fas fa-file";
		} 
		else 
		{
			this.isDirectory = true;
		}
	}

	ngAfterViewInit(): void
	{
		// subtract height of footer and header
		this.dirSection.nativeElement.style.maxHeight = (window.innerHeight - 40 - 100) + "px"; 
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
