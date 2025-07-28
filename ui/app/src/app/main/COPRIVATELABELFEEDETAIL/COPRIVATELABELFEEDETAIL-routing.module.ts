import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { COPRIVATELABELFEEDETAILHomeComponent } from './home/COPRIVATELABELFEEDETAIL-home.component';
import { COPRIVATELABELFEEDETAILNewComponent } from './new/COPRIVATELABELFEEDETAIL-new.component';
import { COPRIVATELABELFEEDETAILDetailComponent } from './detail/COPRIVATELABELFEEDETAIL-detail.component';

const routes: Routes = [
  {path: '', component: COPRIVATELABELFEEDETAILHomeComponent},
  { path: 'new', component: COPRIVATELABELFEEDETAILNewComponent },
  { path: ':ID', component: COPRIVATELABELFEEDETAILDetailComponent,
    data: {
      oPermission: {
        permissionId: 'COPRIVATELABELFEEDETAIL-detail-permissions'
      }
    }
  }
];

export const COPRIVATELABELFEEDETAIL_MODULE_DECLARATIONS = [
    COPRIVATELABELFEEDETAILHomeComponent,
    COPRIVATELABELFEEDETAILNewComponent,
    COPRIVATELABELFEEDETAILDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class COPRIVATELABELFEEDETAILRoutingModule { }