import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PRIVATELABELBILLHomeComponent } from './home/PRIVATELABELBILL-home.component';
import { PRIVATELABELBILLNewComponent } from './new/PRIVATELABELBILL-new.component';
import { PRIVATELABELBILLDetailComponent } from './detail/PRIVATELABELBILL-detail.component';

const routes: Routes = [
  {path: '', component: PRIVATELABELBILLHomeComponent},
  { path: 'new', component: PRIVATELABELBILLNewComponent },
  { path: ':ID', component: PRIVATELABELBILLDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PRIVATELABELBILL-detail-permissions'
      }
    }
  }
];

export const PRIVATELABELBILL_MODULE_DECLARATIONS = [
    PRIVATELABELBILLHomeComponent,
    PRIVATELABELBILLNewComponent,
    PRIVATELABELBILLDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PRIVATELABELBILLRoutingModule { }