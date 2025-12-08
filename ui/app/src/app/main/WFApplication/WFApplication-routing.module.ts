import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFApplicationHomeComponent } from './home/WFApplication-home.component';
import { WFApplicationNewComponent } from './new/WFApplication-new.component';
import { WFApplicationDetailComponent } from './detail/WFApplication-detail.component';
import { OSnackBarConfig } from 'ontimize-web-ngx';

const routes: Routes = [
  {path: '', component: WFApplicationHomeComponent},
  { path: 'new', component: WFApplicationNewComponent },
  { path: ':ApplicationID', component: WFApplicationDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFApplication-detail-permissions'
      }
    }
  },{
    path: ':ApplicationId/RoleAssigment', loadChildren: () => import('../RoleAssigment/RoleAssigment.module').then(m => m.RoleAssigmentModule),
    data: {
        oPermission: {
            permissionId: 'RoleAssigment-detail-permissions'
        }
    }
  },{
    path: ':ApplicationID/WFApplicationMessage', loadChildren: () => import('../WFApplicationMessage/WFApplicationMessage.module').then(m => m.WFApplicationMessageModule),
    data: {
        oPermission: {
            permissionId: 'WFApplicationMessage-detail-permissions'
        }
    }
},{
    path: ':ApplicationID/WFFile', loadChildren: () => import('../WFFile/WFFile.module').then(m => m.WFFileModule),
    data: {
        oPermission: {
            permissionId: 'WFFile-detail-permissions'
        }
    }
},{
    path: ':ApplicationID/WFQuote', loadChildren: () => import('../WFQuote/WFQuote.module').then(m => m.WFQuoteModule),
    data: {
        oPermission: {
            permissionId: 'WFQuote-detail-permissions'
        }
    }
}
];

export const WFAPPLICATION_MODULE_DECLARATIONS = [
    WFApplicationHomeComponent,
    WFApplicationNewComponent,
    WFApplicationDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
  providers: [
    // ...existing providers...
    OSnackBarConfig
  ]
})
export class WFApplicationRoutingModule { }