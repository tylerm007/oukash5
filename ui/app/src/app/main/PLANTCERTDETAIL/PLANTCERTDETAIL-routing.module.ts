import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PLANTCERTDETAILHomeComponent } from './home/PLANTCERTDETAIL-home.component';
import { PLANTCERTDETAILNewComponent } from './new/PLANTCERTDETAIL-new.component';
import { PLANTCERTDETAILDetailComponent } from './detail/PLANTCERTDETAIL-detail.component';

const routes: Routes = [
  {path: '', component: PLANTCERTDETAILHomeComponent},
  { path: 'new', component: PLANTCERTDETAILNewComponent },
  { path: ':ID', component: PLANTCERTDETAILDetailComponent,
    data: {
      oPermission: {
        permissionId: 'PLANTCERTDETAIL-detail-permissions'
      }
    }
  }
];

export const PLANTCERTDETAIL_MODULE_DECLARATIONS = [
    PLANTCERTDETAILHomeComponent,
    PLANTCERTDETAILNewComponent,
    PLANTCERTDETAILDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class PLANTCERTDETAILRoutingModule { }