import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFUserHomeComponent } from './home/WFUser-home.component';
import { WFUserNewComponent } from './new/WFUser-new.component';
import { WFUserDetailComponent } from './detail/WFUser-detail.component';

const routes: Routes = [
  {path: '', component: WFUserHomeComponent},
  { path: 'new', component: WFUserNewComponent },
  { path: ':UserID', component: WFUserDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFUser-detail-permissions'
      }
    }
  }
];

export const WFUSER_MODULE_DECLARATIONS = [
    WFUserHomeComponent,
    WFUserNewComponent,
    WFUserDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFUserRoutingModule { }