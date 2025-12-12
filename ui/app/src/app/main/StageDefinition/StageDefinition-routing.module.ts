import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { StageDefinitionHomeComponent } from './home/StageDefinition-home.component';
import { StageDefinitionNewComponent } from './new/StageDefinition-new.component';
import { StageDefinitionDetailComponent } from './detail/StageDefinition-detail.component';

const routes: Routes = [
  {path: '', component: StageDefinitionHomeComponent},
  { path: 'new', component: StageDefinitionNewComponent },
  { path: ':StageId', component: StageDefinitionDetailComponent,
    data: {
      oPermission: {
        permissionId: 'StageDefinition-detail-permissions'
      }
    }
  },{
    path: ':StageDefinitionId/StageInstance', loadChildren: () => import('../StageInstance/StageInstance.module').then(m => m.StageInstanceModule),
    data: {
        oPermission: {
            permissionId: 'StageInstance-detail-permissions'
        }
    }
},{
    path: ':StageDefinitionId/TaskDefinition', loadChildren: () => import('../TaskDefinition/TaskDefinition.module').then(m => m.TaskDefinitionModule),
    data: {
        oPermission: {
            permissionId: 'TaskDefinition-detail-permissions'
        }
    }
}
];

export const STAGEDEFINITION_MODULE_DECLARATIONS = [
    StageDefinitionHomeComponent,
    StageDefinitionNewComponent,
    StageDefinitionDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StageDefinitionRoutingModule { }