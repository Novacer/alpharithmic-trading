import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { MeanReversionComponent } from './mean-reversion.component';

describe('MeanReversionComponent', () => {
  let component: MeanReversionComponent;
  let fixture: ComponentFixture<MeanReversionComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ MeanReversionComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(MeanReversionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
