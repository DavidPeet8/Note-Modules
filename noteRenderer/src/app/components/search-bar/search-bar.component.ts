import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { FileAccessAPIService } from '@services/file-access-api.service';

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.sass']
})
export class SearchBarComponent implements OnInit {

  searchText: string;
  @Output() searchResultsChange:EventEmitter<Object> = new EventEmitter<Object>();

  constructor(private fileAPI: FileAccessAPIService) { }

  ngOnInit(): void {
  }

  doSearch(): void 
  {
  	console.log(this.searchText);
  	if (this.searchText == "")
  	{
  		this.searchResultsChange.emit(null);
  		return;
  	}

  	this.fileAPI.doSearch(this.searchText, this.searchCallback.bind(this));
  }

  searchCallback(json): void
  {
  	this.searchResultsChange.emit(json);
  }

}
