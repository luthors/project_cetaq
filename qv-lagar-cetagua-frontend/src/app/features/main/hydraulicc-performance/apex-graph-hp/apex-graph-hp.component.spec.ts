import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ApexGraphHpComponent } from './apex-graph-hp.component';

describe('ApexGraphHpComponent', () => {
  let component: ApexGraphHpComponent;
  let fixture: ComponentFixture<ApexGraphHpComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ApexGraphHpComponent]
    });
    fixture = TestBed.createComponent(ApexGraphHpComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
