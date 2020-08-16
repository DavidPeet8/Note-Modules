import { Component, OnInit, Input} from '@angular/core';

@Component({
  selector: 'app-codeview',
  templateUrl: './codeview.component.html',
  styleUrls: ['./codeview.component.sass']
})
export class CodeviewComponent implements OnInit {
	// View Displaying a note
	@Input() filePath: String;
	
	
	constructor() { }

	ngOnInit(): void {}

	getCode(): String 
	{
		// Return URI of resource
		return 'http://localhost:8000/testfile'
	}
}
