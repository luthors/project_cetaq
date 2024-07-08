import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { CookieService } from './cookie.service';

@Injectable({
  providedIn: 'root',
})
export class AuthenticationService {
  private isAuthenticated: boolean = false;
  
  loginUrl: string = environment.loginUrl;
  logoutUrl: string = environment.logoutUrl;

  private readonly TOKEN_KEY = 'authToken';
  private readonly REFRESH_TOKEN = 'refresh-token';

  private refresh: string | null = null;


  constructor(
    private httpClient: HttpClient,
    private router: Router,
    private cookieService: CookieService
  ) {
    if (!this.getToken()) {
      this.router.navigate(['/login']);
    }

  }

  /**
   * Method to log in a user with the provided email and password
   * @param email - the email user
   * @param password - the user password
   * loginUrl is the URL endpoint for user login
   * @returns  A Promise with the result of the login attempt.
   */
  login(email: string, password: string, rememberMe: boolean) {
    return this.httpClient.post<any>(this.loginUrl, { email, password }).pipe(
      tap(response => {
        if (response && response.token) {
          // this.storeToken(response.token);
          if (rememberMe) {
            this.cookieService.setCredentialsCookie(email, password);
          }
        }
      })
    );
  }

  /**
   * This function save the username in the local storage
   * @param {string} username - the user name to be save
   */
  setCurrentUser(response: any ): void {
    localStorage.setItem('currentUser', JSON.stringify(response)); // {name, last_name, email}
    // this.saveToken(response.token)
    // localStorage.setItem('token', response.token);
    
    this.isAuthenticated = true;
  }

  /**
   * This function get username from the local storage
   * @returns a string whit the user
   */
  getCurrentUser(): any {
    return JSON.parse(localStorage.getItem('currentUser') || '{}');
  }

  /**
   * Method to check if the user is athenticated with the isAuthenticated boolean variable
   * @returns a boolean True if the user is authenticated otherwise retunrs false
   */
  isAuthenticatedUser(): boolean {
    return this.isAuthenticated;
  }

  /**
   * Log out the current user updating the athentication state whit flag to false
   * Remove the current user data from the local storage and send a post request to the logout URL
   * logoutUrl is the URL endpoint for user logout
   * @returns  A Promise with the result of the logout attempt.
   */
  logout(): Observable<any> {
    const token = this.getToken()
    const headers = new HttpHeaders({
      'Authorization': 'Bearer ' + token,
    });

    this.isAuthenticated = false;
    localStorage.removeItem('currentUser');
    localStorage.removeItem('refresh-token');
    this.clearToken()
    localStorage.removeItem('exploitation')
    this.cookieService.deleteCredentialsCookie();
    return this.httpClient.post(`${this.logoutUrl}`, {},{ headers: headers });
  }

  /**
   * Method to save the proviede token to the local storage
   * @param {string} token - The token to be saved
   */
  saveToken(token: string): void {
    localStorage.setItem(this.TOKEN_KEY, token);
  }

  saveRefreshToken(token: string): void {
    this.refresh = token
    localStorage.setItem(this.REFRESH_TOKEN, token);
    
  }

  getRefreshToken(): string | null {
    return this.refresh;
  }

  clearRefreshToken():void {
    localStorage.removeItem(this.REFRESH_TOKEN);
  }

  refreshAccessToken(): Observable<any> {
    return this.httpClient.post<any>(`${this.loginUrl}refresh/`, { refresh: this.refresh });
  }
  

  /**
   * Method to get the saved token from the local storage
   * @returns a string with the token value
   */
  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY);
  }

  /**
   * Method to delete the provided token from the local storage
   */
  clearToken(): void {
    localStorage.removeItem(this.TOKEN_KEY);
  }
  saveExploitation(exploitation: string):void{
    localStorage.setItem('exploitation', exploitation)
  }

  getTokenExpiration(token: string ): Date | null {
    try {
      const tokenParts = token.split('.')[1];
      const tokenDecoded = JSON.parse(atob(tokenParts));
      if (tokenDecoded && tokenDecoded.exp) {
        const expirationTimeInSeconds = tokenDecoded.exp;
        return new Date(expirationTimeInSeconds * 1000);
      }
    } catch (error) {
      console.error('Error decoding token:', error);
    }
    return null;
  }

  
}
