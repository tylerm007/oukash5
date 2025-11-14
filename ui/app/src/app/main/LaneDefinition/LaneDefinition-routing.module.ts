import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LaneDefinitionHomeComponent } from './home/LaneDefinition-home.component';
import { LaneDefinitionNewComponent } from './new/LaneDefinition-new.component';
import { LaneDefinitionDetailComponent } from './detail/LaneDefinition-detail.component';

const routes: Routes = [
  {path: '', component: LaneDefinitionHomeComponent},
  { path: 'new', component: LaneDefinitionNewComponent },
  { path: ':LaneId', component: LaneDefinitionDetailComponent,
    data: {
      oPermission: {
        permissionId: 'LaneDefinition-detail-permissions'
      }
    }
  }
];

export const LANEDEFINITION_MODULE_DECLARATIONS = [
    LaneDefinitionHomeComponent,
    LaneDefinitionNewComponent,
    LaneDefinitionDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LaneDefinitionRoutingModule { }