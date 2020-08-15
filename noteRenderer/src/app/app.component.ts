import { Component } from '@angular/core';

@Component({
	selector: 'app-root',
	templateUrl: './app.component.html',
	styleUrls: ['./app.component.sass']
})
export class AppComponent 
{
	title = 'noteRenderer';
	headerStyle = "";

	href(str, event): void
	{
		let location = "";
		switch (str)
		{
			case "github":
				location = "https://github.com/DavidPeet8"
				break;
			case "linkedin":
				location = "https://www.linkedin.com/in/dapeet/";
				break;
			case "website":
				location = "https://davidpeet8.github.io/website/#/";
				break;
		}
		if (event.ctrlKey == true)
		{
			window.open(location, "_blank")
		}
		else 
		{
			window.location.href = location;
		}
	}

	getStyle(): Object
	{
		return 
		({
			maxHeight: window.innerHeight,
			minHeight: window.innerHeight,
			maxWidth: window.innerWidth,
			minWidth: window.innerWidth
		});
	}

	openSettingsModal(): void
	{
		console.log("Settings Hit.");
	}
}
