import { NgModule } from '@angular/core';
import { Router, Routes, RouterModule, NavigationStart } from '@angular/router';
import { HelpModalComponent } from 'app/components/help-modal/help-modal.component';
import { InstallModalComponent } from 'app/components/install-modal/install-modal.component';
import { CodeviewComponent } from 'app/components/codeview/codeview.component';
import { FileAccessAPIService } from '@services/file-access-api.service';

const routes: Routes = [
	{
		path: 'help', component: HelpModalComponent,
	},
	{
		path: 'install', component: InstallModalComponent,
	},
	{
		path: 'note', children: [
			{
				path: '**',
				component: CodeviewComponent
			}
		]
	},
	{
		path: '**', redirectTo: '/', pathMatch: 'full'
	}
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule]
})
export class AppRoutingModule 
{ 
	constructor(private router: Router, private fileAPI: FileAccessAPIService) 
	{
		this.router.events.subscribe(e => {
			if (e instanceof NavigationStart) {
				this.onNavigationStart(e);
			}
		})
	}

	onNavigationStart(event): void
	{
		if (event.url.startsWith('/note/')) 
		{
			let file = '/' + event.url.split('/').slice(2).join('/');
			this.fileAPI.switchActiveFile(file);
		}
	}

}
