import { Component, OnInit, Input, ElementRef, ViewChild} from '@angular/core';
import { FetchRenderEventBusService } from '@services/fetch-render-event-bus.service';
import { FileAccessAPIService } from '@services/file-access-api.service';
import { KatexOptions } from 'ngx-markdown';
 
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
	@ViewChild('scrollContent') scrollContent;
	@ViewChild('displayText') displayText;
	renderContent: String = "";
	options: KatexOptions = {
		displayMode: false,
		throwOnError: false,
		macros: {
			"\\floor": "\\left\\lfloor{#0}\\right\\rfloor",
			"\\ceil": "\\left\lceil{#1}\\right\\rceil",
			"\\paren": "\\left({#1}\\right)",
			"\\brac": "\\left[{#1}\\right]",
			"\\brace": "\\lbrace{#1}\\rbrace"
		}
	}
	
	constructor(private eventBus: FetchRenderEventBusService, private fileAPI: FileAccessAPIService) { }

	ngOnInit(): void 
	{
		this.eventBus.subscribeCodeEvent(this.setCode.bind(this));
	}

	setCode(): void 
	{
		// Fetch the content Required, then set it here
		this.renderContent = this.fileAPI.getCurrentFile();
		this.setOverscroll();
		this.scrollContent.nativeElement.scrollTo(0,0);
	}

	// TODO: Use Angular Observables
	// Problem is that these values are being fetched before the render content is updated, so the overscroll is always one late
	// This should really be implemented using Angular Observables
	setOverscroll(): void
	{
		if(!this.willOverscroll) return;

		let editorScreenHeight = this.codeview.nativeElement.offsetHeight;
		let contentScrollHeight = this.scrollContent.nativeElement.scrollHeight;
		console.log("editorScreenHeight: " + editorScreenHeight);
		console.log("contentScrollHeight: " + contentScrollHeight);
		this.content.nativeElement.style.height = contentScrollHeight + editorScreenHeight - 150 + "px";
	}
}
