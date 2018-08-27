import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TrendFollowComponent } from './trend-follow.component';

describe('TrendFollowComponent', () => {
  let component: TrendFollowComponent;
  let fixture: ComponentFixture<TrendFollowComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TrendFollowComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TrendFollowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
