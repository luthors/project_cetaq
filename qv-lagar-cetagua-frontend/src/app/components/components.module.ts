import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from './sidebar/sidebar.component';
import { NavbarComponent } from './navbar/navbar.component';
import { FooterComponent } from './footer/footer.component';
import { RouterModule } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { FileUploadComponent } from './file.upload/file.upload.component';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { NgxFileDropModule } from 'ngx-file-drop';
import { MatCardModule } from '@angular/material/card';
import { InfoCardComponent } from './info.card/info.card.component';
import { MatMenuModule } from '@angular/material/menu';
import { LoaderModalComponent } from './loader-modal/loader-modal.component';
import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import { MatTooltipModule } from '@angular/material/tooltip';


@NgModule({
  imports: [
    CommonModule,
    RouterModule,
    MatToolbarModule,
    MatButtonModule,
    MatButtonToggleModule,
    MatIconModule,
    MatSidenavModule,
    BrowserAnimationsModule,
    MatListModule,
    MatProgressBarModule,
    MatCardModule,
    NgxFileDropModule,
    MatMenuModule,
    MatProgressSpinnerModule,
    MatTooltipModule,
  ],
  declarations: [
    FooterComponent,
    NavbarComponent,
    SidebarComponent,
    FileUploadComponent,
    InfoCardComponent,
    LoaderModalComponent,
  ],
  exports: [
    FooterComponent,
    NavbarComponent,
    SidebarComponent,
    FileUploadComponent,
  ],
})
export class ComponentsModule {}
