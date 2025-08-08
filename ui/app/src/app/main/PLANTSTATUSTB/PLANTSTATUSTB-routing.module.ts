import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PLANTSTATUSTBHomeComponent } from './home/PLANTSTATUSTB-home.component';
import { PLANTSTATUSTBNewComponent } from './new/PLANTSTATUSTB-new.component';
import { PLANTSTATUSTBDetailComponent } from './detail/PLANTSTATUSTB-detail.component';

const routes: Routes = [
  {path: '', component: PLANTSTATUSTBHomeComponent},
  { path: 'new', component: PLANTSTATUSTBNewComponent },
  { path: ':ID', component: PLANTSTATUSTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PLANTSTATUSTB-detail-permissions'
      }
    }
  }
];

export const PLANTSTATUSTB_MODULE_DECLARATIONS = [
    PLANTSTATUSTBHomeComponent,
    PLANTSTATUSTBNewComponent,
    PLANTSTATUSTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PLANTSTATUSTBRoutingModule { }