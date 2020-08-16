import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
	selector: 'app-render-parent',
	templateUrl: './render-parent.component.html',
	styleUrls: ['./render-parent.component.sass']
})
export class RenderParentComponent implements OnInit 
{
	@ViewChild("dirSection") dirSection: ElementRef;
	@ViewChild("editor") editor: ElementRef;
	@ViewChild("resizeBar") resizeBar: ElementRef;
	dirlist;
	resizeBarY;

	constructor(private http: HttpClient) { }

	ngOnInit(): void {
	}

	ngAfterViewInit(): void
	{
		this.setMaxHeight();
		this.resizeBarY = this.resizeBar.nativeElement.offsetTop;
		//fetch('http://localhost:8000/testfile').then((data) => { data.text().then((d) => {console.log(d);}); });
		fetch('http://localhost:8000/file-list').then((data) => { 
			return data.json();
		}).then((json) => {
			this.dirlist = json.dirs;
		});
	}

	setMaxHeight(): void 
	{
		// subtract height of footer and header
		this.editor.nativeElement.style.maxHeight = (window.innerHeight - 50 - 100) + "px"; 
	}

	onDrag(e): void
	{
		if(e.pageX > 0)
		{
			this.dirSection.nativeElement.style.width = e.pageX + "px";
		}
	}
}
