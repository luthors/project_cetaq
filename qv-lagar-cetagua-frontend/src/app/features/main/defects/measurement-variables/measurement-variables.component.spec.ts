import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MeasurementVariablesComponent } from './measurement-variables.component';

describe('MeasurementVariablesComponent', () => {
  let component: MeasurementVariablesComponent;
  let fixture: ComponentFixture<MeasurementVariablesComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [MeasurementVariablesComponent],
    });
    fixture = TestBed.createComponent(MeasurementVariablesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
