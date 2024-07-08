import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CustomerInformationComponent } from './customer-information.component';
import { MatDialogModule } from '@angular/material/dialog';
import { MatCardModule } from '@angular/material/card';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('CustomerInformationComponent', () => {
  let component: CustomerInformationComponent;
  let fixture: ComponentFixture<CustomerInformationComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CustomerInformationComponent],
      imports: [HttpClientTestingModule, MatDialogModule, MatCardModule ],
    });
    fixture = TestBed.createComponent(CustomerInformationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
