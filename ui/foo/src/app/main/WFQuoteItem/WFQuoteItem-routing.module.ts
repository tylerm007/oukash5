import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFQuoteItemHomeComponent } from './home/WFQuoteItem-home.component';
import { WFQuoteItemNewComponent } from './new/WFQuoteItem-new.component';
import { WFQuoteItemDetailComponent } from './detail/WFQuoteItem-detail.component';

const routes: Routes = [
  {path: '', component: WFQuoteItemHomeComponent},
  { path: 'new', component: WFQuoteItemNewComponent },
  { path: ':QuoteItemID', component: WFQuoteItemDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFQuoteItem-detail-permissions'
      }
    }
  }
];

export const WFQUOTEITEM_MODULE_DECLARATIONS = [
    WFQuoteItemHomeComponent,
    WFQuoteItemNewComponent,
    WFQuoteItemDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFQuoteItemRoutingModule { }