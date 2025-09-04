import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TaskCategoryHomeComponent } from './home/TaskCategory-home.component';
import { TaskCategoryNewComponent } from './new/TaskCategory-new.component';
import { TaskCategoryDetailComponent } from './detail/TaskCategory-detail.component';

const routes: Routes = [
  {path: '', component: TaskCategoryHomeComponent},
  { path: 'new', component: TaskCategoryNewComponent },
  { path: ':TaskCategoryCode', component: TaskCategoryDetailComponent,
    data: {
      oPermission: {
        permissionId: 'TaskCategory-detail-permissions'
      }
    }
  },{
    path: ':TaskCategory/TaskDefinition', loadChildren: () => import('../TaskDefinition/TaskDefinition.module').then(m => m.TaskDefinitionModule),
    data: {
        oPermission: {
            permissionId: 'TaskDefinition-detail-permissions'
        }
    }
}
];

export const TASKCATEGORY_MODULE_DECLARATIONS = [
    TaskCategoryHomeComponent,
    TaskCategoryNewComponent,
    TaskCategoryDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TaskCategoryRoutingModule { }