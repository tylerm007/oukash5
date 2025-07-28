import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { VISITSCOMMENTHomeComponent } from './home/VISITSCOMMENT-home.component';
import { VISITSCOMMENTNewComponent } from './new/VISITSCOMMENT-new.component';
import { VISITSCOMMENTDetailComponent } from './detail/VISITSCOMMENT-detail.component';

const routes: Routes = [
  {path: '', component: VISITSCOMMENTHomeComponent},
  { path: 'new', component: VISITSCOMMENTNewComponent },
  { path: ':ID', component: VISITSCOMMENTDetailComponent,
    data: {
      oPermission: {
        permissionId: 'VISITSCOMMENT-detail-permissions'
      }
    }
  }
];

export const VISITSCOMMENT_MODULE_DECLARATIONS = [
    VISITSCOMMENTHomeComponent,
    VISITSCOMMENTNewComponent,
    VISITSCOMMENTDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class VISITSCOMMENTRoutingModule { }