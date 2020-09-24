import { Component, OnInit } from '@angular/core';
import { FileAccessAPIService } from '@services/file-access-api.service';

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.sass']
})
export class SearchBarComponent implements OnInit {

  searchText: string;

  constructor(private fileAPI: FileAccessAPIService) { }

  ngOnInit(): void {
  }

  doSearch(): void 
  {
  	console.log(this.searchText);
  	this.fileAPI.doSearch(this.searchText, (json) => {console.log(json)});
  }

}
