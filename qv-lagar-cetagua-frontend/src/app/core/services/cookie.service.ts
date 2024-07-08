import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class CookieService {
  private readonly COOKIE_NAME = 'user_credentials';
  private readonly DAYS_TO_EXPIRE = 5

  /**
   * Store user credential in a cookie for remember session. The cookie will expire in a certain number of days
   * DAYS_TO_EXPIRE : Expired cookie days
   * @param email The email to be stored
   * @param password The password to be stored 
   */
  setCredentialsCookie(email: string, password: string): void {
    const credentials = btoa(`${email}:${password}`); // Encode credentials to Base64
    const expirationDate = new Date();
    expirationDate.setDate(expirationDate.getDate() + this.DAYS_TO_EXPIRE); 
    document.cookie = `${this.COOKIE_NAME}=${credentials};expires=${expirationDate.toUTCString()};path=/`;

  }

  /**
   * This fuction returns user credential from the cookie
   * @returns An object with the stored credentials or null if no credential are found
   */
  getCredentialsCookie(): { email: string, password: string } | null {
  const cookieValue = document.cookie
      .split('; ')
      .find(cookie => cookie.startsWith(`${this.COOKIE_NAME}=`));

    if (cookieValue) {
      const credentials = atob(cookieValue.split('=')[1]); // Decode credentials to Base64
      const [email, password] = credentials.split(':');
      return { email, password };
    } else {
      return null;
    }
  }

  /**
   * This function delete the user credential cookie
   */
  deleteCredentialsCookie(): void {
    document.cookie = `${this.COOKIE_NAME}=;expires=Thu, 01 Jan 1970 00:00:00 GMT`; //Delete cookie by setting expiration date to the past
  }
}
