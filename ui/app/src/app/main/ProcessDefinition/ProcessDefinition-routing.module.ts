import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProcessDefinitionHomeComponent } from './home/ProcessDefinition-home.component';
import { ProcessDefinitionNewComponent } from './new/ProcessDefinition-new.component';
import { ProcessDefinitionDetailComponent } from './detail/ProcessDefinition-detail.component';

const routes: Routes = [
  {path: '', component: ProcessDefinitionHomeComponent},
  { path: 'new', component: ProcessDefinitionNewComponent },
  { path: ':ProcessId', component: ProcessDefinitionDetailComponent,
    data: {
      oPermission: {
        permissionId: 'ProcessDefinition-detail-permissions'
      }
    }
  },{
    path: ':ProcessDefinitionId/TaskDefinition', loadChildren: () => import('../TaskDefinition/TaskDefinition.module').then(m => m.TaskDefinitionModule),
    data: {
        oPermission: {
            permissionId: 'TaskDefinition-detail-permissions'
        }
    }
}
];

export const PROCESSDEFINITION_MODULE_DECLARATIONS = [
    ProcessDefinitionHomeComponent,
    ProcessDefinitionNewComponent,
    ProcessDefinitionDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProcessDefinitionRoutingModule { }