import { TestBed } from '@angular/core/testing';

import { CookieService } from './cookie.service';

describe('CookieService', () => {
  let service: CookieService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CookieService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
  it('should store and retrieve user credentials', () => {
    const email = 'testUser@email.com';
    const password = 'testPassword';

    // Store credentials
    service.setCredentialsCookie(email, password);

    // Return credentials
    const storedCredentials = service.getCredentialsCookie();

    expect(storedCredentials).toBeTruthy();
    expect(storedCredentials!.email).toEqual(email);
    expect(storedCredentials!.password).toEqual(password);
  });

  it('should delete user credentials', () => {
    const email = 'testUser';
    const password = 'testPassword';

    // Store credentials
    service.setCredentialsCookie(email, password);

    // Delete credentials
    service.deleteCredentialsCookie();

    // Ensure credentials are deleted
    const storedCredentials = service.getCredentialsCookie();

    expect(storedCredentials).toBeNull();
  });
});
