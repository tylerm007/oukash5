import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PrivateLabelTemplateHomeComponent } from './home/PrivateLabelTemplate-home.component';
import { PrivateLabelTemplateNewComponent } from './new/PrivateLabelTemplate-new.component';
import { PrivateLabelTemplateDetailComponent } from './detail/PrivateLabelTemplate-detail.component';

const routes: Routes = [
  {path: '', component: PrivateLabelTemplateHomeComponent},
  { path: 'new', component: PrivateLabelTemplateNewComponent },
  { path: ':ID', component: PrivateLabelTemplateDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PrivateLabelTemplate-detail-permissions'
      }
    }
  }
];

export const PRIVATELABELTEMPLATE_MODULE_DECLARATIONS = [
    PrivateLabelTemplateHomeComponent,
    PrivateLabelTemplateNewComponent,
    PrivateLabelTemplateDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PrivateLabelTemplateRoutingModule { }