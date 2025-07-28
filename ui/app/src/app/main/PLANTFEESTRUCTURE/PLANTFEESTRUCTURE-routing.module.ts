import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PLANTFEESTRUCTUREHomeComponent } from './home/PLANTFEESTRUCTURE-home.component';
import { PLANTFEESTRUCTURENewComponent } from './new/PLANTFEESTRUCTURE-new.component';
import { PLANTFEESTRUCTUREDetailComponent } from './detail/PLANTFEESTRUCTURE-detail.component';

const routes: Routes = [
  {path: '', component: PLANTFEESTRUCTUREHomeComponent},
  { path: 'new', component: PLANTFEESTRUCTURENewComponent },
  { path: ':ID', component: PLANTFEESTRUCTUREDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PLANTFEESTRUCTURE-detail-permissions'
      }
    }
  }
];

export const PLANTFEESTRUCTURE_MODULE_DECLARATIONS = [
    PLANTFEESTRUCTUREHomeComponent,
    PLANTFEESTRUCTURENewComponent,
    PLANTFEESTRUCTUREDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PLANTFEESTRUCTURERoutingModule { }