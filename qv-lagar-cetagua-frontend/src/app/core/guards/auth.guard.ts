import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, RouterStateSnapshot, UrlTree } from '@angular/router';
import { AuthenticationService } from '../services/authentication.service';
import { Observable } from 'rxjs';
import { EXPLOITATION_GRANADA_ID, environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private authService: AuthenticationService, private router: Router) {}

  /**
   * Guard to prevent unauthorized access to a route
   * If value is EXPLOITATION_GRANADA_ID allows access to the route  
   * @returns Retunr boolean indicating whether the route can be activated or not. 
   */
  canActivate(): boolean {
    const token = this.authService.getToken();
    const refreshToken = this.authService.getRefreshToken();
    const exploitationWithAccess = localStorage.getItem('exploitation');

    if (!token) {
      this.router.navigate(['/login']);
      return false;
    }

    if (exploitationWithAccess === EXPLOITATION_GRANADA_ID) {
      return true; // Allows access to the route
    } else {
      // Redirect to main module
      this.router.navigate(['/main']);
      return false; //  Prevent access to the route
    }


    
  }

}
