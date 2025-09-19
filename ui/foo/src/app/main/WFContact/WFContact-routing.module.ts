import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFContactHomeComponent } from './home/WFContact-home.component';
import { WFContactNewComponent } from './new/WFContact-new.component';
import { WFContactDetailComponent } from './detail/WFContact-detail.component';

const routes: Routes = [
  {path: '', component: WFContactHomeComponent},
  { path: 'new', component: WFContactNewComponent },
  { path: ':ContactID', component: WFContactDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFContact-detail-permissions'
      }
    }
  }
];

export const WFCONTACT_MODULE_DECLARATIONS = [
    WFContactHomeComponent,
    WFContactNewComponent,
    WFContactDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFContactRoutingModule { }