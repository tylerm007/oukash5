import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { StageInstanceHomeComponent } from './home/StageInstance-home.component';
import { StageInstanceNewComponent } from './new/StageInstance-new.component';
import { StageInstanceDetailComponent } from './detail/StageInstance-detail.component';

const routes: Routes = [
  {path: '', component: StageInstanceHomeComponent},
  { path: 'new', component: StageInstanceNewComponent },
  { path: ':StageInstanceId', component: StageInstanceDetailComponent,
    data: {
      oPermission: {
        permissionId: 'StageInstance-detail-permissions'
      }
    }
  },{
    path: ':StageId/TaskInstance', loadChildren: () => import('../TaskInstance/TaskInstance.module').then(m => m.TaskInstanceModule),
    data: {
        oPermission: {
            permissionId: 'TaskInstance-detail-permissions'
        }
    }
}
];

export const STAGEINSTANCE_MODULE_DECLARATIONS = [
    StageInstanceHomeComponent,
    StageInstanceNewComponent,
    StageInstanceDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StageInstanceRoutingModule { }