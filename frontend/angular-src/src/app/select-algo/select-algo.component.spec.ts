import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SelectAlgoComponent } from './select-algo.component';

describe('SelectAlgoComponent', () => {
  let component: SelectAlgoComponent;
  let fixture: ComponentFixture<SelectAlgoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SelectAlgoComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SelectAlgoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
