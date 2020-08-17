import { Injectable } from '@angular/core';
import { FileAccessAPIService } from '@services/file-access-api.service';

@Injectable({
  providedIn: 'root'
})
export class FetchRenderEventBusService {
	dirEventSubs = [];
	codeEventSubs = [];

	constructor(private fileAPI: FileAccessAPIService) 
	{
		fileAPI.setPublishMethod({ 
			dirEvent: this._publishDirEvent.bind(this), 
			codeEvent:  this._publishCodeEvent.bind(this)
		});
	}

	// Subscribe to new data changes
	subscribeDirEvent(notifyFunc): void
	{
		this.dirEventSubs.push(notifyFunc);
	}

	subscribeCodeEvent(notifyFunc): void
	{
		this.codeEventSubs.push(notifyFunc);
	}

	_publishDirEvent(): void 
	{
		this._publish(this.dirEventSubs);
	}

	_publishCodeEvent(): void 
	{
		this._publish(this.codeEventSubs);
	}

	_publish (publishFuncArray): void
	{
		for (let sub of publishFuncArray) sub();
	}
}
