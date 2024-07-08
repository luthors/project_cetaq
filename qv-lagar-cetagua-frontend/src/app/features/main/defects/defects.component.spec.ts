import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DefectsComponent } from './defects.component';

describe('DefectsComponent', () => {
  let component: DefectsComponent;
  let fixture: ComponentFixture<DefectsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DefectsComponent],
    });
    fixture = TestBed.createComponent(DefectsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
