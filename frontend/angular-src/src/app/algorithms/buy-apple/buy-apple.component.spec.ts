import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BuyAppleComponent } from './buy-apple.component';

describe('BuyAppleComponent', () => {
  let component: BuyAppleComponent;
  let fixture: ComponentFixture<BuyAppleComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BuyAppleComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BuyAppleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
