import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MiniCRMActionHomeComponent } from './home/MiniCRMAction-home.component';
import { MiniCRMActionNewComponent } from './new/MiniCRMAction-new.component';
import { MiniCRMActionDetailComponent } from './detail/MiniCRMAction-detail.component';

const routes: Routes = [
  {path: '', component: MiniCRMActionHomeComponent},
  { path: 'new', component: MiniCRMActionNewComponent },
  { path: ':ID', component: MiniCRMActionDetailComponent,
    data: {
      oPermission: {
        permissionId: 'MiniCRMAction-detail-permissions'
      }
    }
  }
];

export const MINICRMACTION_MODULE_DECLARATIONS = [
    MiniCRMActionHomeComponent,
    MiniCRMActionNewComponent,
    MiniCRMActionDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MiniCRMActionRoutingModule { }