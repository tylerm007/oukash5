import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PLANTFEECOMMENTHomeComponent } from './home/PLANTFEECOMMENT-home.component';
import { PLANTFEECOMMENTNewComponent } from './new/PLANTFEECOMMENT-new.component';
import { PLANTFEECOMMENTDetailComponent } from './detail/PLANTFEECOMMENT-detail.component';

const routes: Routes = [
  {path: '', component: PLANTFEECOMMENTHomeComponent},
  { path: 'new', component: PLANTFEECOMMENTNewComponent },
  { path: ':ID', component: PLANTFEECOMMENTDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PLANTFEECOMMENT-detail-permissions'
      }
    }
  }
];

export const PLANTFEECOMMENT_MODULE_DECLARATIONS = [
    PLANTFEECOMMENTHomeComponent,
    PLANTFEECOMMENTNewComponent,
    PLANTFEECOMMENTDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PLANTFEECOMMENTRoutingModule { }