import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PERSONJOBSTATUSTBHomeComponent } from './home/PERSONJOBSTATUSTB-home.component';
import { PERSONJOBSTATUSTBNewComponent } from './new/PERSONJOBSTATUSTB-new.component';
import { PERSONJOBSTATUSTBDetailComponent } from './detail/PERSONJOBSTATUSTB-detail.component';

const routes: Routes = [
  {path: '', component: PERSONJOBSTATUSTBHomeComponent},
  { path: 'new', component: PERSONJOBSTATUSTBNewComponent },
  { path: ':ID', component: PERSONJOBSTATUSTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PERSONJOBSTATUSTB-detail-permissions'
      }
    }
  }
];

export const PERSONJOBSTATUSTB_MODULE_DECLARATIONS = [
    PERSONJOBSTATUSTBHomeComponent,
    PERSONJOBSTATUSTBNewComponent,
    PERSONJOBSTATUSTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PERSONJOBSTATUSTBRoutingModule { }