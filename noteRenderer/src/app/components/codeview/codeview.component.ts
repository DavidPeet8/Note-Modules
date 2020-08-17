import { Component, OnInit, Input, ElementRef, ViewChild} from '@angular/core';
import { FetchRenderEventBusService } from '@services/fetch-render-event-bus.service';
import { FileAccessAPIService } from '@services/file-access-api.service';

@Component({
  selector: 'app-codeview',
  templateUrl: './codeview.component.html',
  styleUrls: ['./codeview.component.sass']
})
export class CodeviewComponent implements OnInit {
	// View Displaying a note
	@Input() willOverscroll: boolean = true;
	@ViewChild('codeview') codeview; 
	@ViewChild('content') content;
	@ViewChild('displayText') displayText;
	renderContent: String = "";
	
	constructor(private eventBus: FetchRenderEventBusService, private fileAPI: FileAccessAPIService) { }

	ngOnInit(): void 
	{
		this.eventBus.subscribeCodeEvent(this.setCode.bind(this));
	}

	setCode(): void 
	{
		// Make the request for the first note to display or just leave it empty
		// Fetch the content Required, then set it here
		this.renderContent = this.fileAPI.getCurrentFile();
	}

	setOverscroll(): void
	{
		if(!this.willOverscroll) return;
		
		let editorScreenHeight = this.codeview.nativeElement.offsetHeight;
		let contentScrollHeight = this.content.nativeElement.scrollHeight;
		this.content.nativeElement.style.height = contentScrollHeight + editorScreenHeight - 150 + "px";
	}
}
