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
    path: ':ApplicationID/WFActivityLog', loadChildren: () => import('../WFActivityLog/WFActivityLog.module').then(m => m.WFActivityLogModule),
    data: {
        oPermission: {
            permissionId: 'WFActivityLog-detail-permissions'
        }
    }
},{
    path: ':ApplicationID/WFApplicationComment', loadChildren: () => import('../WFApplicationComment/WFApplicationComment.module').then(m => m.WFApplicationCommentModule),
    data: {
        oPermission: {
            permissionId: 'WFApplicationComment-detail-permissions'
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
    path: ':ApplicationID/WFCompany', loadChildren: () => import('../WFCompany/WFCompany.module').then(m => m.WFCompanyModule),
    data: {
        oPermission: {
            permissionId: 'WFCompany-detail-permissions'
        }
    }
},{
    path: ':ApplicationID/WFContact', loadChildren: () => import('../WFContact/WFContact.module').then(m => m.WFContactModule),
    data: {
        oPermission: {
            permissionId: 'WFContact-detail-permissions'
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
    path: ':ApplicationID/WFIngredient', loadChildren: () => import('../WFIngredient/WFIngredient.module').then(m => m.WFIngredientModule),
    data: {
        oPermission: {
            permissionId: 'WFIngredient-detail-permissions'
        }
    }
},{
    path: ':ApplicationID/WFProduct', loadChildren: () => import('../WFProduct/WFProduct.module').then(m => m.WFProductModule),
    data: {
        oPermission: {
            permissionId: 'WFProduct-detail-permissions'
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