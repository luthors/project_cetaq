import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DefectsComponent } from './defects/defects.component';
import { HydrauliccPerformanceComponent } from './hydraulicc-performance/hydraulicc-performance.component';
import { CustomerInformationComponent } from './customer-information/customer-information.component';
import { MainComponent } from './main.component';
import { UserProfileComponent } from './user-profile/user-profile.component';
import { AuthGuard } from 'src/app/core/guards/auth.guard';

const routes: Routes = [
  {
    path: '',
    component: MainComponent,
    children: [
      { path: 'main', component: DefectsComponent },
      {
        path: 'rendimiento-hidraulico',
        component: HydrauliccPerformanceComponent,
      },
      {
        path: 'asignacion-usuarios-a-sectores',
        component: CustomerInformationComponent,
        canActivate: [AuthGuard]
      },
      {
        path: 'user-profile',
        component: UserProfileComponent,
      },

      { path: '', redirectTo: 'main', pathMatch: 'full' },
    ],
    // canActivate: [AuthGuard],
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class MainRoutingModule {}
