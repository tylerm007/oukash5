import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { OWNSTBHomeComponent } from './home/OWNSTB-home.component';
import { OWNSTBNewComponent } from './new/OWNSTB-new.component';
import { OWNSTBDetailComponent } from './detail/OWNSTB-detail.component';

const routes: Routes = [
  {path: '', component: OWNSTBHomeComponent},
  { path: 'new', component: OWNSTBNewComponent },
  { path: ':ID', component: OWNSTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'OWNSTB-detail-permissions'
      }
    }
  }
];

export const OWNSTB_MODULE_DECLARATIONS = [
    OWNSTBHomeComponent,
    OWNSTBNewComponent,
    OWNSTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class OWNSTBRoutingModule { }