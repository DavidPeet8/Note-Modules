import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RenderParentComponent } from './render-parent.component';

describe('RenderParentComponent', () => {
  let component: RenderParentComponent;
  let fixture: ComponentFixture<RenderParentComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RenderParentComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RenderParentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
