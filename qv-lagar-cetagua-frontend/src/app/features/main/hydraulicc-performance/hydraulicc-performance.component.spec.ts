import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HydrauliccPerformanceComponent } from './hydraulicc-performance.component';

describe('HydrauliccPerformanceComponent', () => {
  let component: HydrauliccPerformanceComponent;
  let fixture: ComponentFixture<HydrauliccPerformanceComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [HydrauliccPerformanceComponent],
    });
    fixture = TestBed.createComponent(HydrauliccPerformanceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
