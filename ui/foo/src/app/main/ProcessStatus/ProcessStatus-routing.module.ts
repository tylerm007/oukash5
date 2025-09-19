import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProcessStatusHomeComponent } from './home/ProcessStatus-home.component';
import { ProcessStatusNewComponent } from './new/ProcessStatus-new.component';
import { ProcessStatusDetailComponent } from './detail/ProcessStatus-detail.component';

const routes: Routes = [
  {path: '', component: ProcessStatusHomeComponent},
  { path: 'new', component: ProcessStatusNewComponent },
  { path: ':StatusCode', component: ProcessStatusDetailComponent,
    data: {
      oPermission: {
        permissionId: 'ProcessStatus-detail-permissions'
      }
    }
  },{
    path: ':Status/ProcessInstance', loadChildren: () => import('../ProcessInstance/ProcessInstance.module').then(m => m.ProcessInstanceModule),
    data: {
        oPermission: {
            permissionId: 'ProcessInstance-detail-permissions'
        }
    }
}
];

export const PROCESSSTATUS_MODULE_DECLARATIONS = [
    ProcessStatusHomeComponent,
    ProcessStatusNewComponent,
    ProcessStatusDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProcessStatusRoutingModule { }