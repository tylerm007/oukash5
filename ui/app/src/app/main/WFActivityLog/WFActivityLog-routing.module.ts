import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFActivityLogHomeComponent } from './home/WFActivityLog-home.component';
import { WFActivityLogNewComponent } from './new/WFActivityLog-new.component';
import { WFActivityLogDetailComponent } from './detail/WFActivityLog-detail.component';

const routes: Routes = [
  {path: '', component: WFActivityLogHomeComponent},
  { path: 'new', component: WFActivityLogNewComponent },
  { path: ':ActivityID', component: WFActivityLogDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFActivityLog-detail-permissions'
      }
    }
  }
];

export const WFACTIVITYLOG_MODULE_DECLARATIONS = [
    WFActivityLogHomeComponent,
    WFActivityLogNewComponent,
    WFActivityLogDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFActivityLogRoutingModule { }