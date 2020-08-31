import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HelpModalComponent } from 'app/components/help-modal/help-modal.component';


const routes: Routes = [
	{
		path: 'help', component: HelpModalComponent
	},
	/*{
		// This route for loading each note based on url / note name
		//path: 'note/*', component: 
	}*/
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule]
})
export class AppRoutingModule 
{ 

}
