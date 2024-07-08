import { Component } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';
import { AuthenticationService } from 'src/app/core/services/authentication.service';
import { MapService } from 'src/app/core/services/map.service';
import { ProfileService } from 'src/app/core/services/profile.service';
import { MANUAL_NAME, environment } from 'src/environments/environment';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.scss']
})
export class UserProfileComponent {

  hide = true;
  hideConfirm = true;
  // user: any;
  user = {
    name: '',
    last_name: '',
    email: '',
    id:0,
  };
  exploitation = ''
  
  changePasswordForm!: FormGroup;

  constructor(private authService: AuthenticationService, private profileService: ProfileService, private formBuilder: FormBuilder, private mapService: MapService) {
    this.user = this.authService.getCurrentUser();
    
    ;
  }
  /**
   * Initializes the password change form with appropriate validators.
   */
  ngOnInit(): void {
    this.changePasswordForm = this.formBuilder.group({
      // currentPassword: ['', Validators.required],
      newPassword: ['', [Validators.required, Validators.minLength(8), this.validatePasswordFormat]],
      confirmPassword: ['', Validators.required]
    }, { validator: this.confirmPassword });
    this.mapService.getMap(parseInt(localStorage.getItem('exploitation')|| '0', 10)).subscribe(
      data =>{
        this.exploitation = data.name
      }
    );
  }

  /**
   * Update personal information function
   */
  saveData(){
    this.profileService.updateProfile(this.user.name,this.user.last_name,this.user.email, this.user.id).subscribe(
      response => {
        this.authService.setCurrentUser(this.user);
        Swal.fire('Guardado', 'Datos actualizado exitosamente', 'success')

      },
      error => {
        if (error.status === 401)Swal.fire('Error', 'Error en la autenticación del usuario', 'error');
        else Swal.fire('Error', 'No se pude realizar la actualización de datos', 'error')
      }
    )
  }

  /**
   * Change password function 
   */
  changePassword() {

    if (this.changePasswordForm && this.changePasswordForm.valid) {
      const newPasswordControl = this.changePasswordForm.get('newPassword');
      const confirmPasswordControl = this.changePasswordForm.get('confirmPassword');
  
      if (newPasswordControl && confirmPasswordControl) {
        const newPassword = newPasswordControl.value;
        const confirmPassword = confirmPasswordControl.value;
        this.profileService.updatePassword(newPassword, confirmPassword, this.user.id).subscribe(
          response => {
            Swal.fire('¡Guardado!', '¡Contraseña actualizada con éxito!', 'success');
          },
          error => {
            if (error.status === 401) {
              Swal.fire('Error', 'Error en la autenticación del usuario', 'error');
            } else {
              Swal.fire('Error', 'No se puede realizar la actualización de contraseña', 'error');
            }
          }
        );
      }
    }
    else {
      // Invalid form
      Swal.fire('Error', 'Por favor, completa el formulario correctamente', 'error');
    }
  }
  /**
   * Custom validation function to ensure password confirmation
   * @param formGroup The form group containing the passwords
   * @returns An object if validation fails, null otherwise
   */
  confirmPassword(formGroup: FormGroup) {
    const newPasswordControl = formGroup.get('newPassword');
    const confirmPasswordControl = formGroup.get('confirmPassword');

    if (newPasswordControl && confirmPasswordControl) {
      const newPassword = newPasswordControl.value;
      const confirmPassword = confirmPasswordControl.value;

      // Return null if password match, otherwise return object
      return newPassword === confirmPassword ? null : { noCoinciden: true };
    }
    return null; // Return null if passwords match
  }

  /**
   * Function to validate the password format.
   * @param control The form control that contains the password value
   * regex is a regular expresion that indicates the required format
   * @returns An object if the password doesn't conform to the specified format, otherwise returns null
  */
  validatePasswordFormat(control: any) {
    const regex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$/;
    return regex.test(control.value) ? null : { invalidFormato: true };
  }

  /**
   * Function to download the user manual
   * manualUserUrl The url of the user manual
   * manualName The name for the download file
   * link The temporary link to download the file
   */
  downloadDocument() {
    const manualUserUrl = environment.manualUserUrl; 
    const link = document.createElement('a');
    link.href = manualUserUrl;
    link.download = MANUAL_NAME;
    link.click();
  }

  /**
   * Handles form submission
  */
  onSubmit() {
    if (this.changePasswordForm.valid) {
      this.changePassword();
    } 
    else {
      const newPassword = this.changePasswordForm.get('newPassword');
      const confirmPassword = this.changePasswordForm.get('confirmPassword');
      // Check if passwords have a valid format 
      if(newPassword?.invalid || confirmPassword?.invalid){
        Swal.fire('Error', 'La contraseña debe tener al menos 8 caracteres, una letra, un número y un carácter especial.', 'error');
        return; //Stop execution if passwords do not match
      }
      // Check if passwords match
      else if (newPassword?.value && confirmPassword?.value && newPassword != confirmPassword) {
          // Show error message using Swal.fire
          Swal.fire('Error', 'Las contraseñas no coinciden', 'error');
          return; //Stop execution if passwords do not match
      }
      else Swal.fire('Error', 'Datos incompletos o erroneos', 'error');
    }
  }
}
