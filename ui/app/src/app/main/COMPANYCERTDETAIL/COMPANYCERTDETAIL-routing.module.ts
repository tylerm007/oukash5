import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { COMPANYCERTDETAILHomeComponent } from './home/COMPANYCERTDETAIL-home.component';
import { COMPANYCERTDETAILNewComponent } from './new/COMPANYCERTDETAIL-new.component';
import { COMPANYCERTDETAILDetailComponent } from './detail/COMPANYCERTDETAIL-detail.component';

const routes: Routes = [
  {path: '', component: COMPANYCERTDETAILHomeComponent},
  { path: 'new', component: COMPANYCERTDETAILNewComponent },
  { path: ':ID', component: COMPANYCERTDETAILDetailComponent,
    data: {
      oPermission: {
        permissionId: 'COMPANYCERTDETAIL-detail-permissions'
      }
    }
  }
];

export const COMPANYCERTDETAIL_MODULE_DECLARATIONS = [
    COMPANYCERTDETAILHomeComponent,
    COMPANYCERTDETAILNewComponent,
    COMPANYCERTDETAILDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class COMPANYCERTDETAILRoutingModule { }