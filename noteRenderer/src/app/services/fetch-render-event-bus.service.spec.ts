import { TestBed } from '@angular/core/testing';

import { FetchRenderEventBusService } from './fetch-render-event-bus.service';

describe('FetchRenderEventBusService', () => {
  let service: FetchRenderEventBusService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FetchRenderEventBusService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
