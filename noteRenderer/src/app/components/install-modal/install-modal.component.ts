import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-install-modal',
  templateUrl: './install-modal.component.html',
  styleUrls: ['./install-modal.component.sass']
})
export class InstallModalComponent implements OnInit {

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
