import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFActivityStatusHomeComponent } from './home/WFActivityStatus-home.component';
import { WFActivityStatusNewComponent } from './new/WFActivityStatus-new.component';
import { WFActivityStatusDetailComponent } from './detail/WFActivityStatus-detail.component';

const routes: Routes = [
  {path: '', component: WFActivityStatusHomeComponent},
  { path: 'new', component: WFActivityStatusNewComponent },
  { path: ':StatusCode', component: WFActivityStatusDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFActivityStatus-detail-permissions'
      }
    }
  },{
    path: ':Status/WFActivityLog', loadChildren: () => import('../WFActivityLog/WFActivityLog.module').then(m => m.WFActivityLogModule),
    data: {
        oPermission: {
            permissionId: 'WFActivityLog-detail-permissions'
        }
    }
}
];

export const WFACTIVITYSTATUS_MODULE_DECLARATIONS = [
    WFActivityStatusHomeComponent,
    WFActivityStatusNewComponent,
    WFActivityStatusDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFActivityStatusRoutingModule { }