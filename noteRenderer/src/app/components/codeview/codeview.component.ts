import { Component, OnInit, Input, ElementRef, ViewChild} from '@angular/core';

@Component({
  selector: 'app-codeview',
  templateUrl: './codeview.component.html',
  styleUrls: ['./codeview.component.sass']
})
export class CodeviewComponent implements OnInit {
	// View Displaying a note
	@Input() filePath: String;
	@Input() willOverscroll: boolean = true;
	@ViewChild('codeview') codeview; 
	@ViewChild('content') content;
	@ViewChild('markdown') markdown;
	
	constructor() { }

	ngOnInit(): void 
	{
		// Make the request for the first note to display or just leave it empty
	}

	getCode(): String 
	{
		// Return URI of resource
		return 'http://localhost:8000/testfile'
	}

	setOverscroll(): void
	{
		if(!this.willOverscroll) return;
		
		let editorScreenHeight = this.codeview.nativeElement.offsetHeight;
		let contentScrollHeight = this.content.nativeElement.scrollHeight;
		console.log("editorScreenHeight: " + editorScreenHeight);
		console.log("contentScrollHeight: " + contentScrollHeight);
		this.content.nativeElement.style.height = contentScrollHeight + editorScreenHeight - 150 + "px";
	}
}
