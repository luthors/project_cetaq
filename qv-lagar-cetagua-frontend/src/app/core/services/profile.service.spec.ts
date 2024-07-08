import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing'; 
import { ProfileService } from './profile.service';
import { environment } from 'src/environments/environment';

describe('ProfileService', () => {
  let service: ProfileService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [ProfileService]
    });
    service = TestBed.inject(ProfileService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });
  it('should be created', () => {
    expect(service).toBeTruthy();
  });
  
  it('should send update request with correct data', () => {
    const mockData = { name: 'John', lastName: 'Doe', email: 'john@example.com' };
    const mockId = 1;
  
    service.updateProfile(mockData.name, mockData.lastName, mockData.email, mockId).subscribe(response => {
      expect(response).toBeTruthy();
    });
  
    const request = httpMock.expectOne(`${environment.updateProfileUrl}${mockId}/`);
    expect(request.request.method).toBe('PUT');
    expect(request.request.body).toEqual(mockData);
    
    request.flush({}); // Mock response data if needed
  });
  
  it('should send update password request with correct data', () => {
    const mockPasswordData = { password: 'newpassword', password2: 'newpassword' };
    const mockId = 1;
  
    service.updatePassword(mockPasswordData.password, mockPasswordData.password2, mockId).subscribe(response => {
      expect(response).toBeTruthy();
    });
  
    const request = httpMock.expectOne(`${environment.updateProfileUrl}${mockId}/set_password/`);
    expect(request.request.method).toBe('POST');
    expect(request.request.body).toEqual(mockPasswordData);
    // Add authorization header expectation
    expect(request.request.headers.get('Authorization')).toBe('Bearer ' + localStorage.getItem('authToken'));
  
    request.flush({}); // Mock response data if needed
  });
  
});