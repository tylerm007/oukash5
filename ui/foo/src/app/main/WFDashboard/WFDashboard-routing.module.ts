import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFDashboardHomeComponent } from './home/WFDashboard-home.component';
import { WFDashboardNewComponent } from './new/WFDashboard-new.component';
import { WFDashboardDetailComponent } from './detail/WFDashboard-detail.component';

const routes: Routes = [
  {path: '', component: WFDashboardHomeComponent},
  { path: 'new', component: WFDashboardNewComponent },
  { path: ':ID', component: WFDashboardDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFDashboard-detail-permissions'
      }
    }
  },{
    path: ':WFDashboardID/WFApplication', loadChildren: () => import('../WFApplication/WFApplication.module').then(m => m.WFApplicationModule),
    data: {
        oPermission: {
            permissionId: 'WFApplication-detail-permissions'
        }
    }
}
];

export const WFDASHBOARD_MODULE_DECLARATIONS = [
    WFDashboardHomeComponent,
    WFDashboardNewComponent,
    WFDashboardDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFDashboardRoutingModule { }