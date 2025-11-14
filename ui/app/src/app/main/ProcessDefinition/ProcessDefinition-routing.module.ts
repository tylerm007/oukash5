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
    path: ':ProcessId/StageDefinition', loadChildren: () => import('../StageDefinition/StageDefinition.module').then(m => m.StageDefinitionModule),
    data: {
        oPermission: {
            permissionId: 'StageDefinition-detail-permissions'
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