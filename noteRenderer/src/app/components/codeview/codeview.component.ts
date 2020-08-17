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
	
	constructor() { }

	ngOnInit(): void {}

	getCode(): String 
	{
		// Return URI of resource
		return 'http://localhost:8000/testfile'
	}

	setOverscroll(): void
	{
		if(!this.willOverscroll) return;

		// if height is large enough, then 
		console.log("Height: ")
		console.log(this.content.nativeElement.scrollHeight);
		
		if (this.content.nativeElement.scrollHeight) 
		{
			let editorScreenHeight = this.codeview.nativeElement.offsetHeight;
			let contentScrollHeight = this.content.nativeElement.scrollHeight;
			console.log("editorScreenHeight: " + editorScreenHeight);
			console.log("contentScrollHeight: " + contentScrollHeight);
			this.content.nativeElement.style.height = contentScrollHeight + editorScreenHeight - 150 + "px";
		}
	}
}
