import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LoginComponent } from './login.component';
import { AuthenticationService } from 'src/app/core/services/authentication.service';
import { FormBuilder, ReactiveFormsModule } from '@angular/forms';
import { ComponentsModule } from 'src/app/components/components.module';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrowserModule } from '@angular/platform-browser';
import {MatCheckboxModule} from '@angular/material/checkbox';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('LoginComponent', () => {
  let component: LoginComponent;
  let fixture: ComponentFixture<LoginComponent>;
  let authService : AuthenticationService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LoginComponent],
      imports : [HttpClientTestingModule, ReactiveFormsModule, MatCardModule, MatInputModule, MatButtonModule, MatIconModule, BrowserAnimationsModule, BrowserModule, MatCheckboxModule ],
      providers : [FormBuilder, AuthenticationService,ComponentsModule],
    });

    fixture = TestBed.createComponent(LoginComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
    authService = TestBed.inject(AuthenticationService)
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('invalid form', ()=>{
    const username = component.loginForm.controls['email']
    username.setValue('demo@correo.com')
    expect(component.loginForm.invalid).toBeTrue();
  });

  it('valid form', ()=>{
    const username = component.loginForm.controls['email']
    const password = component.loginForm.controls['password']
    username.setValue('demo@correo.com')
    password.setValue('password')
    expect(component.loginForm.invalid).toBeFalse();
  });
});
