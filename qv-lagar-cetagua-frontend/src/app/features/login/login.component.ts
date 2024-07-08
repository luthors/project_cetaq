import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthenticationService } from 'src/app/core/services/authentication.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  errorMessage: string = '';
  loginForm: FormGroup;
  recoveryForm: FormGroup;
  showPasswordRecoveryForm: boolean = false;
  showForgotPasswordForm = false;
  rememberMe: boolean = false;
  hide = true;
  private authToken: string | null = null; // Para almacenar el token en memoria de la app en caso de no querer recordar la sesion 
  private refreshToken: string | null = null; // Para almacenar el token en memoria de la app en caso de no querer recordar la sesion 
  resetUrl: string = environment.resetUrl; 
  
  constructor(
    private fb: FormBuilder,
    private router: Router,
    private authService: AuthenticationService
  ) {
    this.loginForm = this.fb.group({
      email: ['', Validators.required],
      password: ['', Validators.required],
      rememberMeControl: [false],
    });
    this.recoveryForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
    });
  }


  login(): void {
    const { email, password, rememberMeControl } = this.loginForm.value;
    this.authService.login(email, password, rememberMeControl).subscribe(
      response => {
        this.authService.saveToken(response.token)
        this.authService.saveRefreshToken(response['refresh-token'])
        this.authService.setCurrentUser(response.user);
        this.authService.saveExploitation(response.exploitation)
        this.errorMessage = '';
        this.router.navigate(['/main']);
      },
      error => {
        this.errorMessage =
          'Error al iniciar sesión. Por favor, verifica tus credenciales.';
      }
    );
  }

  showRecoveryForm(): void {
    this.showPasswordRecoveryForm = true;
  }

  showLoginForm(): void {
    this.showPasswordRecoveryForm = false;
  }

  redirectToResetPassword(){
    window.open(`${this.resetUrl}`, '_blank');
  }
}
