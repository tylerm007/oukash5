import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PLANTTBHomeComponent } from './home/PLANTTB-home.component';
import { PLANTTBNewComponent } from './new/PLANTTB-new.component';
import { PLANTTBDetailComponent } from './detail/PLANTTB-detail.component';

const routes: Routes = [
  {path: '', component: PLANTTBHomeComponent},
  { path: 'new', component: PLANTTBNewComponent },
  { path: ':PLANT_ID', component: PLANTTBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PLANTTB-detail-permissions'
      }
    }
  }
];

export const PLANTTB_MODULE_DECLARATIONS = [
    PLANTTBHomeComponent,
    PLANTTBNewComponent,
    PLANTTBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PLANTTBRoutingModule { }