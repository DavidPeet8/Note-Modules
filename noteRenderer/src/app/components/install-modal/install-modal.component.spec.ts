import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InstallModalComponent } from './install-modal.component';

describe('InstallModalComponent', () => {
  let component: InstallModalComponent;
  let fixture: ComponentFixture<InstallModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InstallModalComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InstallModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
