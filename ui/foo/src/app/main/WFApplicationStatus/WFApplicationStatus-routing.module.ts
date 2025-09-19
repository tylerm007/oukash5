import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFApplicationStatusHomeComponent } from './home/WFApplicationStatus-home.component';
import { WFApplicationStatusNewComponent } from './new/WFApplicationStatus-new.component';
import { WFApplicationStatusDetailComponent } from './detail/WFApplicationStatus-detail.component';

const routes: Routes = [
  {path: '', component: WFApplicationStatusHomeComponent},
  { path: 'new', component: WFApplicationStatusNewComponent },
  { path: ':StatusCode', component: WFApplicationStatusDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFApplicationStatus-detail-permissions'
      }
    }
  },{
    path: ':Status/WFApplication', loadChildren: () => import('../WFApplication/WFApplication.module').then(m => m.WFApplicationModule),
    data: {
        oPermission: {
            permissionId: 'WFApplication-detail-permissions'
        }
    }
}
];

export const WFAPPLICATIONSTATUS_MODULE_DECLARATIONS = [
    WFApplicationStatusHomeComponent,
    WFApplicationStatusNewComponent,
    WFApplicationStatusDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFApplicationStatusRoutingModule { }