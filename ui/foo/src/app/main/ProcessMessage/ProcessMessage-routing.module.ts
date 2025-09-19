import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProcessMessageHomeComponent } from './home/ProcessMessage-home.component';
import { ProcessMessageNewComponent } from './new/ProcessMessage-new.component';
import { ProcessMessageDetailComponent } from './detail/ProcessMessage-detail.component';

const routes: Routes = [
  {path: '', component: ProcessMessageHomeComponent},
  { path: 'new', component: ProcessMessageNewComponent },
  { path: ':MessageId', component: ProcessMessageDetailComponent,
    data: {
      oPermission: {
        permissionId: 'ProcessMessage-detail-permissions'
      }
    }
  }
];

export const PROCESSMESSAGE_MODULE_DECLARATIONS = [
    ProcessMessageHomeComponent,
    ProcessMessageNewComponent,
    ProcessMessageDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProcessMessageRoutingModule { }