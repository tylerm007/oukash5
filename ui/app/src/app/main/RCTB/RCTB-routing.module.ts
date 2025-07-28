import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RCTBHomeComponent } from './home/RCTB-home.component';
import { RCTBNewComponent } from './new/RCTB-new.component';
import { RCTBDetailComponent } from './detail/RCTB-detail.component';

const routes: Routes = [
  {path: '', component: RCTBHomeComponent},
  { path: 'new', component: RCTBNewComponent },
  { path: ':ID', component: RCTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'RCTB-detail-permissions'
      }
    }
  }
];

export const RCTB_MODULE_DECLARATIONS = [
    RCTBHomeComponent,
    RCTBNewComponent,
    RCTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RCTBRoutingModule { }