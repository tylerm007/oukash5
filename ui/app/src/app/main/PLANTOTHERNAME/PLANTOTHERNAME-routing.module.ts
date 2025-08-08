import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PLANTOTHERNAMEHomeComponent } from './home/PLANTOTHERNAME-home.component';
import { PLANTOTHERNAMENewComponent } from './new/PLANTOTHERNAME-new.component';
import { PLANTOTHERNAMEDetailComponent } from './detail/PLANTOTHERNAME-detail.component';

const routes: Routes = [
  {path: '', component: PLANTOTHERNAMEHomeComponent},
  { path: 'new', component: PLANTOTHERNAMENewComponent },
  { path: ':ALIAS_ID', component: PLANTOTHERNAMEDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PLANTOTHERNAME-detail-permissions'
      }
    }
  }
];

export const PLANTOTHERNAME_MODULE_DECLARATIONS = [
    PLANTOTHERNAMEHomeComponent,
    PLANTOTHERNAMENewComponent,
    PLANTOTHERNAMEDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PLANTOTHERNAMERoutingModule { }