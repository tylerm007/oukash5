import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { COMPANYFEESTRUCTUREHomeComponent } from './home/COMPANYFEESTRUCTURE-home.component';
import { COMPANYFEESTRUCTURENewComponent } from './new/COMPANYFEESTRUCTURE-new.component';
import { COMPANYFEESTRUCTUREDetailComponent } from './detail/COMPANYFEESTRUCTURE-detail.component';

const routes: Routes = [
  {path: '', component: COMPANYFEESTRUCTUREHomeComponent},
  { path: 'new', component: COMPANYFEESTRUCTURENewComponent },
  { path: ':ID', component: COMPANYFEESTRUCTUREDetailComponent,
    data: {
      oPermission: {
        permissionId: 'COMPANYFEESTRUCTURE-detail-permissions'
      }
    }
  }
];

export const COMPANYFEESTRUCTURE_MODULE_DECLARATIONS = [
    COMPANYFEESTRUCTUREHomeComponent,
    COMPANYFEESTRUCTURENewComponent,
    COMPANYFEESTRUCTUREDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class COMPANYFEESTRUCTURERoutingModule { }