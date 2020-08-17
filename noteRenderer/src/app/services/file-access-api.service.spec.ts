import { TestBed } from '@angular/core/testing';

import { FileAccessAPIService } from './file-access-api.service';

describe('FileAccessAPIService', () => {
  let service: FileAccessAPIService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FileAccessAPIService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
