import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ComponentsModule } from './components/components.module';
import { MainModule } from './features/main/main.module';
import { LoginModule } from './features/login/login.module';
import { AuthenticationService } from './core/services/authentication.service';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { FileUploadComponent } from './components/file.upload/file.upload.component';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgxFileDropModule } from 'ngx-file-drop';
import { AuthInterceptor } from './core/services/auth.interceptor';

@NgModule({
  declarations: [AppComponent],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    NgxChartsModule,
    AppRoutingModule,
    ComponentsModule,
    MainModule,
    LoginModule,
    HttpClientModule,
    NgxFileDropModule,
    
  ],
  providers: [AuthenticationService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
