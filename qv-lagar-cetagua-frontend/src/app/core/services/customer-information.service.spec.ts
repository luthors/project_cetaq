import { TestBed } from '@angular/core/testing';

import { CustomerInformationService } from './customer-information.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('CustomerInformationService', () => {
  let service: CustomerInformationService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule]
    });
    service = TestBed.inject(CustomerInformationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
