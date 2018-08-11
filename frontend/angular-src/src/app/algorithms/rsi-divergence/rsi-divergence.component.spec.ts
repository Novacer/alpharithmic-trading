import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RsiDivergenceComponent } from './rsi-divergence.component';

describe('RsiDivergenceComponent', () => {
  let component: RsiDivergenceComponent;
  let fixture: ComponentFixture<RsiDivergenceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RsiDivergenceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RsiDivergenceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
