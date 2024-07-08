import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpResponse,
  HttpErrorResponse
} from '@angular/common/http';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { catchError, filter, switchMap, take, tap } from 'rxjs/operators';
import { AuthenticationService } from './authentication.service';
import { Router } from '@angular/router';
import { CookieService } from './cookie.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  private isRefreshing = false;
  private refreshTokenSubject: BehaviorSubject<any> = new BehaviorSubject<any>(null);

  constructor(private authService: AuthenticationService, private router: Router, private cookieService: CookieService) {}

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const token = this.authService.getToken();
    const refresh = this.authService.getRefreshToken();

    if (token) {
      request = this.addTokenToRequest(request, token);
    }

    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 401 && !request.url.includes('/refresh')) {
          // If response is Unauthorized (401) and the request is different for refreshing
          return this.handle401Error(request, next);
        } else {
          return throwError(error);
        }
      })
    );
  }

  private addTokenToRequest(request: HttpRequest<any>, token: string): HttpRequest<any> {
    return request.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`
      }
    });
  }

  private handle401Error(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    if (!this.isRefreshing) {
      this.isRefreshing = true;
      this.refreshTokenSubject.next(null);

      return this.authService.refreshAccessToken().pipe(
        switchMap((response: any) => {
          this.isRefreshing = false;
          this.refreshTokenSubject.next(response.access);
          this.authService.saveToken(response.access)
          this.authService.saveRefreshToken(response.refresh)
          return next.handle(this.addTokenToRequest(request, response.access));
        }),
        catchError((error: any) => {
          this.isRefreshing = false;
          // Check for the existence of the cookie credentials
            const credentials = this.cookieService.getCredentialsCookie();
            if(credentials){
              // Login using credentials
            return this.authService.login(credentials.email, credentials.password, true).pipe(
              switchMap((loginResponse: any) => {
                // Retry the original request with new token
                this.authService.saveToken(loginResponse.token)
                this.authService.saveRefreshToken(loginResponse['refresh-token'])
                return next.handle(this.addTokenToRequest(request, loginResponse.token));
              }),
              catchError((loginError: any) => {
                // Clear session and redirect to login page if login fails
                this.authService.logout();
                this.router.navigate(['/login']);
                return throwError(loginError);
              })
            );
            }
            
          // } 
          else {
            // Clear session and redirect to login page if no credentials cookie found
            this.authService.logout();
            this.router.navigate(['/login']);
            return throwError(error);
          }
        })
      );
    } else {
      return this.refreshTokenSubject.pipe(
        filter(token => token !== null),
        take(1),
        switchMap(access => {
          return next.handle(this.addTokenToRequest(request, access));
        })
      );
    }
  }
}