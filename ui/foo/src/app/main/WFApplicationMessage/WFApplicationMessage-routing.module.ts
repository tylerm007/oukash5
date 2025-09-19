import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFApplicationMessageHomeComponent } from './home/WFApplicationMessage-home.component';
import { WFApplicationMessageNewComponent } from './new/WFApplicationMessage-new.component';
import { WFApplicationMessageDetailComponent } from './detail/WFApplicationMessage-detail.component';

const routes: Routes = [
  {path: '', component: WFApplicationMessageHomeComponent},
  { path: 'new', component: WFApplicationMessageNewComponent },
  { path: ':MessageID', component: WFApplicationMessageDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFApplicationMessage-detail-permissions'
      }
    }
  }
];

export const WFAPPLICATIONMESSAGE_MODULE_DECLARATIONS = [
    WFApplicationMessageHomeComponent,
    WFApplicationMessageNewComponent,
    WFApplicationMessageDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFApplicationMessageRoutingModule { }