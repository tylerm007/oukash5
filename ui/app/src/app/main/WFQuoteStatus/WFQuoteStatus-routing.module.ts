import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFQuoteStatusHomeComponent } from './home/WFQuoteStatus-home.component';
import { WFQuoteStatusNewComponent } from './new/WFQuoteStatus-new.component';
import { WFQuoteStatusDetailComponent } from './detail/WFQuoteStatus-detail.component';

const routes: Routes = [
  {path: '', component: WFQuoteStatusHomeComponent},
  { path: 'new', component: WFQuoteStatusNewComponent },
  { path: ':StatusCode', component: WFQuoteStatusDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFQuoteStatus-detail-permissions'
      }
    }
  },{
    path: ':Status/WFQuote', loadChildren: () => import('../WFQuote/WFQuote.module').then(m => m.WFQuoteModule),
    data: {
        oPermission: {
            permissionId: 'WFQuote-detail-permissions'
        }
    }
}
];

export const WFQUOTESTATUS_MODULE_DECLARATIONS = [
    WFQuoteStatusHomeComponent,
    WFQuoteStatusNewComponent,
    WFQuoteStatusDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFQuoteStatusRoutingModule { }