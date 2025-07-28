import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { USEDIN1TBHomeComponent } from './home/USEDIN1TB-home.component';
import { USEDIN1TBNewComponent } from './new/USEDIN1TB-new.component';
import { USEDIN1TBDetailComponent } from './detail/USEDIN1TB-detail.component';

const routes: Routes = [
  {path: '', component: USEDIN1TBHomeComponent},
  { path: 'new', component: USEDIN1TBNewComponent },
  { path: ':ID', component: USEDIN1TBDetailComponent,
    data: {
      oPermission: {
        permissionId: 'USEDIN1TB-detail-permissions'
      }
    }
  }
];

export const USEDIN1TB_MODULE_DECLARATIONS = [
    USEDIN1TBHomeComponent,
    USEDIN1TBNewComponent,
    USEDIN1TBDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class USEDIN1TBRoutingModule { }