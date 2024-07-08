import { ComponentFixture, TestBed, fakeAsync, tick } from '@angular/core/testing';

import { UserProfileComponent } from './user-profile.component';
import { ReactiveFormsModule, FormBuilder, FormsModule } from '@angular/forms';
import { ProfileService } from 'src/app/core/services/profile.service';
import { of } from 'rxjs';
import Swal from 'sweetalert2';
import { HttpClientModule } from '@angular/common/http';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

describe('UserProfileComponent', () => {
  let component: UserProfileComponent;
  let fixture: ComponentFixture<UserProfileComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [UserProfileComponent],
      imports: [ReactiveFormsModule, HttpClientModule, MatCardModule,MatChipsModule, MatIconModule,
         MatTabsModule, MatFormFieldModule, FormsModule, MatInputModule]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UserProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize changePasswordForm with appropriate validators', () => {
    expect(component.changePasswordForm).toBeDefined();
    expect(component.changePasswordForm.get('newPassword')).toBeTruthy();
    expect(component.changePasswordForm.get('confirmPassword')).toBeTruthy();
  });

  it('should have custom validator for password confirmation', () => {
    const formGroup = component.changePasswordForm;
    formGroup.setValue({ newPassword: 'password', confirmPassword: 'password' });
    expect(formGroup.valid).toBeTrue();

    formGroup.setValue({ newPassword: 'password', confirmPassword: 'wrongpassword' });
    expect(formGroup.valid).toBeFalse();
    expect(formGroup.errors).toEqual({ noCoinciden: true });
  });

  it('should show error message if passwords do not match on form submission', () => {
    spyOn(window, 'alert'); // Spy on window.alert
    component.changePasswordForm.setValue({ newPassword: 'password', confirmPassword: 'wrongpassword' });
    component.onSubmit();
    expect(window.alert).toHaveBeenCalledWith('Las contraseñas no coinciden');
  });

  it('should show error message if form is invalid on form submission', () => {
    spyOn(window, 'alert');
    component.onSubmit();
    expect(window.alert).toHaveBeenCalledWith('Por favor, completa el formulario correctamente');
  });
});