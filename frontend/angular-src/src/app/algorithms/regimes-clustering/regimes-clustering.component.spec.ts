import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RegimesClusteringComponent } from './regimes-clustering.component';

describe('RegimesClusteringComponent', () => {
  let component: RegimesClusteringComponent;
  let fixture: ComponentFixture<RegimesClusteringComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RegimesClusteringComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RegimesClusteringComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
