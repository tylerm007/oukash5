import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFFileHomeComponent } from './home/WFFile-home.component';
import { WFFileNewComponent } from './new/WFFile-new.component';
import { WFFileDetailComponent } from './detail/WFFile-detail.component';

const routes: Routes = [
  {path: '', component: WFFileHomeComponent},
  { path: 'new', component: WFFileNewComponent },
  { path: ':FileID', component: WFFileDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFFile-detail-permissions'
      }
    }
  }
];

export const WFFILE_MODULE_DECLARATIONS = [
    WFFileHomeComponent,
    WFFileNewComponent,
    WFFileDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFFileRoutingModule { }