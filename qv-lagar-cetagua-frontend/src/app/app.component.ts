import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from './core/services/authentication.service';
import { Router } from '@angular/router';
import { CookieService } from './core/services/cookie.service';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit{
  title = 'front';
  constructor(private authService: AuthenticationService, private router: Router, private cookieService:CookieService) {
  }

  ngOnInit(): void {
    // If credencial are found, the system try to login automatically
    const savedCredentials = this.cookieService.getCredentialsCookie();
    if (savedCredentials) {
      this.authService.login(savedCredentials.email, savedCredentials.password, true).subscribe(
        response => {
          this.authService.saveToken(response.token)
          this.authService.saveRefreshToken(response['refresh-token'])
        },
        error => {
          Swal.fire('Error','Error al iniciar sesión. Por favor, verifica tus credenciales.' ,'error');
          this.router.navigate(['/main']);
        }
      );
    }
  }

}
