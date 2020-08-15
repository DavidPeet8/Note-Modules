import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';

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

	constructor() { }

	ngOnInit(): void {
	}

	ngAfterViewInit(): void
	{
		this.setMaxHeight();
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
