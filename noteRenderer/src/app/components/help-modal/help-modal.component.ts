import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';


@Component({
  selector: 'app-help-modal',
  templateUrl: './help-modal.component.html',
  styleUrls: ['./help-modal.component.sass']
})
export class HelpModalComponent implements OnInit {

  constructor(private router: Router) { }

  ngOnInit(): void {
  }

  stopPropagation(event) 
  {
  	// Prevent event from bubbling
  	event.stopPropagation();
  }

  closeModal() 
  {
  	this.router.navigate(['']); // Navigate back
  }

}
