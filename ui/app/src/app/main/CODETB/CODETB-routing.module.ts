import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CODETBHomeComponent } from './home/CODETB-home.component';
import { CODETBNewComponent } from './new/CODETB-new.component';
import { CODETBDetailComponent } from './detail/CODETB-detail.component';

const routes: Routes = [
  {path: '', component: CODETBHomeComponent},
  { path: 'new', component: CODETBNewComponent },
  { path: ':CodeId', component: CODETBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'CODETB-detail-permissions'
      }
    }
  }
];

export const CODETB_MODULE_DECLARATIONS = [
    CODETBHomeComponent,
    CODETBNewComponent,
    CODETBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CODETBRoutingModule { }