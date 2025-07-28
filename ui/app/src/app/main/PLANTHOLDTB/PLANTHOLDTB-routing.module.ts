import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PLANTHOLDTBHomeComponent } from './home/PLANTHOLDTB-home.component';
import { PLANTHOLDTBNewComponent } from './new/PLANTHOLDTB-new.component';
import { PLANTHOLDTBDetailComponent } from './detail/PLANTHOLDTB-detail.component';

const routes: Routes = [
  {path: '', component: PLANTHOLDTBHomeComponent},
  { path: 'new', component: PLANTHOLDTBNewComponent },
  { path: ':ID', component: PLANTHOLDTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PLANTHOLDTB-detail-permissions'
      }
    }
  }
];

export const PLANTHOLDTB_MODULE_DECLARATIONS = [
    PLANTHOLDTBHomeComponent,
    PLANTHOLDTBNewComponent,
    PLANTHOLDTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PLANTHOLDTBRoutingModule { }