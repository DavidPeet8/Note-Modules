import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { FetchRenderEventBusService } from '@services/fetch-render-event-bus.service';
import { FileAccessAPIService } from '@services/file-access-api.service';

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
	dirlist; resizeBarY;
	searchResults = null;

	constructor(private eventBus: FetchRenderEventBusService, private fileAPI: FileAccessAPIService) { }

	ngOnInit(): void 
	{
		this.eventBus.subscribeDirEvent(this.setDirList.bind(this));
	}

	ngAfterViewInit(): void
	{
		this.setMaxHeight();
		this.resizeBarY = this.resizeBar.nativeElement.offsetTop;
		
	}

	setDirList(): void 
	{
		this.dirlist = this.fileAPI.getDirList();
		console.log("DirList: ", this.dirlist)
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

	onNewSearchResults(json): void
	{
		console.log(json);
		if (json == null) { this.searchResults = null; }
		let results = Object.entries(json).sort((a,b) => { return Number(a[1]) - Number(b[1]); })
		console.log("RESULTS: ", results);
		this.searchResults = results.map(entry => entry[0]);
		console.log("SearchResults: ", this.searchResults);
	}	
}
