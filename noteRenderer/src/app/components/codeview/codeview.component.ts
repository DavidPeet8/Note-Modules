import { Component, OnInit, Input, ViewChild, AfterViewInit, ElementRef } from '@angular/core';

@Component({
  selector: 'app-codeview',
  templateUrl: './codeview.component.html',
  styleUrls: ['./codeview.component.sass']
})
export class CodeviewComponent implements OnInit, AfterViewInit {
	// View Displaying a note
	@Input() filePath: String;
	@ViewChild("codeSection") codeSection: ElementRef;
	
	constructor() { }

	ngOnInit(): void 
	{
		// Set max height here
	}

  	ngAfterViewInit(): void
	{
		// subtract height of footer and header
		this.codeSection.nativeElement.style.maxHeight = (window.innerHeight - 40 - 100 )+ "px"; 
		console.log("Code View Max Height: " + (window.innerHeight -40-100));
	}

}
