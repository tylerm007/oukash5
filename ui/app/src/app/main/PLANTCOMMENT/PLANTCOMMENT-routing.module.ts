import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PLANTCOMMENTHomeComponent } from './home/PLANTCOMMENT-home.component';
import { PLANTCOMMENTNewComponent } from './new/PLANTCOMMENT-new.component';
import { PLANTCOMMENTDetailComponent } from './detail/PLANTCOMMENT-detail.component';

const routes: Routes = [
  {path: '', component: PLANTCOMMENTHomeComponent},
  { path: 'new', component: PLANTCOMMENTNewComponent },
  { path: ':ID', component: PLANTCOMMENTDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PLANTCOMMENT-detail-permissions'
      }
    }
  }
];

export const PLANTCOMMENT_MODULE_DECLARATIONS = [
    PLANTCOMMENTHomeComponent,
    PLANTCOMMENTNewComponent,
    PLANTCOMMENTDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PLANTCOMMENTRoutingModule { }