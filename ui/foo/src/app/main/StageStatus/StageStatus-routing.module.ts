import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { StageStatusHomeComponent } from './home/StageStatus-home.component';
import { StageStatusNewComponent } from './new/StageStatus-new.component';
import { StageStatusDetailComponent } from './detail/StageStatus-detail.component';

const routes: Routes = [
  {path: '', component: StageStatusHomeComponent},
  { path: 'new', component: StageStatusNewComponent },
  { path: ':StatusCode', component: StageStatusDetailComponent,
    data: {
      oPermission: {
        permissionId: 'StageStatus-detail-permissions'
      }
    }
  },{
    path: ':Status/StageInstance', loadChildren: () => import('../StageInstance/StageInstance.module').then(m => m.StageInstanceModule),
    data: {
        oPermission: {
            permissionId: 'StageInstance-detail-permissions'
        }
    }
}
];

export const STAGESTATUS_MODULE_DECLARATIONS = [
    StageStatusHomeComponent,
    StageStatusNewComponent,
    StageStatusDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class StageStatusRoutingModule { }