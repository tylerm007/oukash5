import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFQuoteHomeComponent } from './home/WFQuote-home.component';
import { WFQuoteNewComponent } from './new/WFQuote-new.component';
import { WFQuoteDetailComponent } from './detail/WFQuote-detail.component';

const routes: Routes = [
  {path: '', component: WFQuoteHomeComponent},
  { path: 'new', component: WFQuoteNewComponent },
  { path: ':QuoteID', component: WFQuoteDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFQuote-detail-permissions'
      }
    }
  },{
    path: ':QuoteID/WFQuoteItem', loadChildren: () => import('../WFQuoteItem/WFQuoteItem.module').then(m => m.WFQuoteItemModule),
    data: {
        oPermission: {
            permissionId: 'WFQuoteItem-detail-permissions'
        }
    }
}
];

export const WFQUOTE_MODULE_DECLARATIONS = [
    WFQuoteHomeComponent,
    WFQuoteNewComponent,
    WFQuoteDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFQuoteRoutingModule { }