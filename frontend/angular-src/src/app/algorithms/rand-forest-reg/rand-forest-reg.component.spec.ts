import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RandForestRegComponent } from './rand-forest-reg.component';

describe('RandForestRegComponent', () => {
  let component: RandForestRegComponent;
  let fixture: ComponentFixture<RandForestRegComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RandForestRegComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RandForestRegComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
