import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LabelOptionHomeComponent } from './home/LabelOption-home.component';
import { LabelOptionNewComponent } from './new/LabelOption-new.component';
import { LabelOptionDetailComponent } from './detail/LabelOption-detail.component';

const routes: Routes = [
  {path: '', component: LabelOptionHomeComponent},
  { path: 'new', component: LabelOptionNewComponent },
  { path: ':LabelID', component: LabelOptionDetailComponent,
    data: {
      oPermission: {
        permissionId: 'LabelOption-detail-permissions'
      }
    }
  }
];

export const LABELOPTION_MODULE_DECLARATIONS = [
    LabelOptionHomeComponent,
    LabelOptionNewComponent,
    LabelOptionDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LabelOptionRoutingModule { }