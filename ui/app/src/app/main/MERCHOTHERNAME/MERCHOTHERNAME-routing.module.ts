import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MERCHOTHERNAMEHomeComponent } from './home/MERCHOTHERNAME-home.component';
import { MERCHOTHERNAMENewComponent } from './new/MERCHOTHERNAME-new.component';
import { MERCHOTHERNAMEDetailComponent } from './detail/MERCHOTHERNAME-detail.component';

const routes: Routes = [
  {path: '', component: MERCHOTHERNAMEHomeComponent},
  { path: 'new', component: MERCHOTHERNAMENewComponent },
  { path: ':ID', component: MERCHOTHERNAMEDetailComponent,
    data: {
      oPermission: {
        permissionId: 'MERCHOTHERNAME-detail-permissions'
      }
    }
  }
];

export const MERCHOTHERNAME_MODULE_DECLARATIONS = [
    MERCHOTHERNAMEHomeComponent,
    MERCHOTHERNAMENewComponent,
    MERCHOTHERNAMEDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MERCHOTHERNAMERoutingModule { }