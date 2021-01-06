import { Component, OnInit, Input, ElementRef, ViewChild } from '@angular/core';
import { FetchRenderEventBusService } from '@services/fetch-render-event-bus.service';
import { FileAccessAPIService } from '@services/file-access-api.service';
import { Renderer } from '@services/renderer.service';

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
	renderedContent: string;

	constructor(private eventBus: FetchRenderEventBusService, private fileAPI: FileAccessAPIService, private renderer: Renderer) { }

	ngOnInit(): void {
		this.eventBus.subscribeCodeEvent(this.setCode.bind(this));
	}

	setCode(): void {
		// Fetch the content Required, then set it here
		let rawContent = this.fileAPI.getCurrentFile();
		// Ideally make this call asynchronous
		this.renderedContent = this.renderer.renderToString(rawContent);

		this.codeview.nativeElement.scrollTop = 0;
		setTimeout(this.setOverscroll.bind(this), 300);
	}

	// TODO: Use Angular Observables
	// Problem is that these values are being fetched before the render content is updated, so the overscroll is always one late
	// This should really be implemented using Angular Observables
	setOverscroll(): void {
		if (!this.willOverscroll) return;

		let editorScreenHeight = this.codeview.nativeElement.offsetHeight;
		let contentScrollHeight = this.scrollContent.nativeElement.scrollHeight;
		this.content.nativeElement.style.height = contentScrollHeight + editorScreenHeight - 150 + "px";
	}
}
