import { Component } from '@angular/core';
import { Router } from '@angular/router';


@Component({
	selector: 'app-root',
	templateUrl: './app.component.html',
	styleUrls: ['./app.component.sass']
})
export class AppComponent 
{
	title = 'noteRenderer';
	headerStyle = "";

	constructor(private router: Router) {}

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
		if (event.ctrlKey)
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

	openHelpModal(): void
	{
		this.router.navigate(["help"]);
	}
}
