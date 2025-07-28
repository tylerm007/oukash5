import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MERCHCOMMENTHomeComponent } from './home/MERCHCOMMENT-home.component';
import { MERCHCOMMENTNewComponent } from './new/MERCHCOMMENT-new.component';
import { MERCHCOMMENTDetailComponent } from './detail/MERCHCOMMENT-detail.component';

const routes: Routes = [
  {path: '', component: MERCHCOMMENTHomeComponent},
  { path: 'new', component: MERCHCOMMENTNewComponent },
  { path: ':ID', component: MERCHCOMMENTDetailComponent,
    data: {
      oPermission: {
        permissionId: 'MERCHCOMMENT-detail-permissions'
      }
    }
  }
];

export const MERCHCOMMENT_MODULE_DECLARATIONS = [
    MERCHCOMMENTHomeComponent,
    MERCHCOMMENTNewComponent,
    MERCHCOMMENTDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MERCHCOMMENTRoutingModule { }