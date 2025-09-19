import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { COMPANYTBHomeComponent } from './home/COMPANYTB-home.component';
import { COMPANYTBNewComponent } from './new/COMPANYTB-new.component';
import { COMPANYTBDetailComponent } from './detail/COMPANYTB-detail.component';

const routes: Routes = [
  {path: '', component: COMPANYTBHomeComponent},
  { path: 'new', component: COMPANYTBNewComponent },
  { path: ':COMPANY_ID', component: COMPANYTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'COMPANYTB-detail-permissions'
      }
    }
  },{
    path: ':COMPANY_ID/PLANTTB', loadChildren: () => import('../PLANTTB/PLANTTB.module').then(m => m.PLANTTBModule),
    data: {
        oPermission: {
            permissionId: 'PLANTTB-detail-permissions'
        }
    }
},{
    path: ':COMPANY_ID/OWNSTB', loadChildren: () => import('../OWNSTB/OWNSTB.module').then(m => m.OWNSTBModule),
    data: {
        oPermission: {
            permissionId: 'OWNSTB-detail-permissions'
        }
    }
}
];

export const COMPANYTB_MODULE_DECLARATIONS = [
    COMPANYTBHomeComponent,
    COMPANYTBNewComponent,
    COMPANYTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class COMPANYTBRoutingModule { }