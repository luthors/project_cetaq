import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DefectsComponent } from './defects/defects.component';
import { MainComponent } from './main.component';
import { ComponentsModule } from 'src/app/components/components.module';
import { AppRoutingModule } from 'src/app/app-routing.module';
import { MatCardModule } from '@angular/material/card';
import { MapComponent } from './defects/map/map.component';
import { MatIconModule } from '@angular/material/icon';
import { MeasurementVariablesComponent } from './defects/measurement-variables/measurement-variables.component';
import { HydrauliccPerformanceComponent } from './hydraulicc-performance/hydraulicc-performance.component';
import { CustomerInformationComponent } from './customer-information/customer-information.component';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MainRoutingModule } from './main-routing.module';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { MatFormFieldModule } from '@angular/material/form-field';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { NgApexchartsModule } from 'ng-apexcharts';
import { ApexGraphComponent } from './defects/apex-graph-defects/apex-graph.component';
import { ApexGraphHpComponent } from './hydraulicc-performance/apex-graph-hp/apex-graph-hp.component';
import { UserProfileComponent } from './user-profile/user-profile.component';
import {MatTabsModule} from '@angular/material/tabs';
import {MatDividerModule} from '@angular/material/divider';
import {MatChipsModule} from '@angular/material/chips';

@NgModule({
  declarations: [
    DefectsComponent,
    MainComponent,
    MapComponent,
    MeasurementVariablesComponent,
    HydrauliccPerformanceComponent,
    CustomerInformationComponent,
    ApexGraphComponent,
    ApexGraphHpComponent,
    UserProfileComponent,
  ],
  imports: [
    CommonModule,
    ComponentsModule,
    MainRoutingModule,
    MatInputModule,
    MatButtonModule,
    MatCardModule,
    NgxChartsModule,
    MatIconModule,
    MatSidenavModule,
    MatFormFieldModule,
    ReactiveFormsModule,
    FormsModule,
    BrowserAnimationsModule,
    MatSelectModule,
    MatDialogModule,
    MatSlideToggleModule,
    MatCheckboxModule,
    MatTableModule,
    MatPaginatorModule,
    NgApexchartsModule,
    MatTabsModule,
    MatDividerModule,
    MatChipsModule,
  ],
})
export class MainModule {}
