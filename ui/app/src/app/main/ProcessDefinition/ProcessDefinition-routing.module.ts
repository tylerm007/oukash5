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
    path: ':ProcessId/LaneDefinition', loadChildren: () => import('../LaneDefinition/LaneDefinition.module').then(m => m.LaneDefinitionModule),
    data: {
        oPermission: {
            permissionId: 'LaneDefinition-detail-permissions'
        }
    }
},{
    path: ':ProcessId/ProcessInstance', loadChildren: () => import('../ProcessInstance/ProcessInstance.module').then(m => m.ProcessInstanceModule),
    data: {
        oPermission: {
            permissionId: 'ProcessInstance-detail-permissions'
        }
    }
},{
    path: ':ProcessId/TaskDefinition', loadChildren: () => import('../TaskDefinition/TaskDefinition.module').then(m => m.TaskDefinitionModule),
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