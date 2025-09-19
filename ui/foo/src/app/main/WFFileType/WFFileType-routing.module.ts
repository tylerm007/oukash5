import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFFileTypeHomeComponent } from './home/WFFileType-home.component';
import { WFFileTypeNewComponent } from './new/WFFileType-new.component';
import { WFFileTypeDetailComponent } from './detail/WFFileType-detail.component';

const routes: Routes = [
  {path: '', component: WFFileTypeHomeComponent},
  { path: 'new', component: WFFileTypeNewComponent },
  { path: ':FileType', component: WFFileTypeDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFFileType-detail-permissions'
      }
    }
  },{
    path: ':FileType/WFFile', loadChildren: () => import('../WFFile/WFFile.module').then(m => m.WFFileModule),
    data: {
        oPermission: {
            permissionId: 'WFFile-detail-permissions'
        }
    }
}
];

export const WFFILETYPE_MODULE_DECLARATIONS = [
    WFFileTypeHomeComponent,
    WFFileTypeNewComponent,
    WFFileTypeDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFFileTypeRoutingModule { }