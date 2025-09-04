import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProcessMessageTypeHomeComponent } from './home/ProcessMessageType-home.component';
import { ProcessMessageTypeNewComponent } from './new/ProcessMessageType-new.component';
import { ProcessMessageTypeDetailComponent } from './detail/ProcessMessageType-detail.component';

const routes: Routes = [
  {path: '', component: ProcessMessageTypeHomeComponent},
  { path: 'new', component: ProcessMessageTypeNewComponent },
  { path: ':MessageTypeCode', component: ProcessMessageTypeDetailComponent,
    data: {
      oPermission: {
        permissionId: 'ProcessMessageType-detail-permissions'
      }
    }
  },{
    path: ':MessageType/ProcessMessage', loadChildren: () => import('../ProcessMessage/ProcessMessage.module').then(m => m.ProcessMessageModule),
    data: {
        oPermission: {
            permissionId: 'ProcessMessage-detail-permissions'
        }
    }
}
];

export const PROCESSMESSAGETYPE_MODULE_DECLARATIONS = [
    ProcessMessageTypeHomeComponent,
    ProcessMessageTypeNewComponent,
    ProcessMessageTypeDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProcessMessageTypeRoutingModule { }