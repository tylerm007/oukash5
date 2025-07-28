import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProducedIn1TbHomeComponent } from './home/ProducedIn1Tb-home.component';
import { ProducedIn1TbNewComponent } from './new/ProducedIn1Tb-new.component';
import { ProducedIn1TbDetailComponent } from './detail/ProducedIn1Tb-detail.component';

const routes: Routes = [
  {path: '', component: ProducedIn1TbHomeComponent},
  { path: 'new', component: ProducedIn1TbNewComponent },
  { path: ':ID', component: ProducedIn1TbDetailComponent,
    data: {
      oPermission: {
        permissionId: 'ProducedIn1Tb-detail-permissions'
      }
    }
  },{
    path: ':prid/ProductJobLineItem', loadChildren: () => import('../ProductJobLineItem/ProductJobLineItem.module').then(m => m.ProductJobLineItemModule),
    data: {
        oPermission: {
            permissionId: 'ProductJobLineItem-detail-permissions'
        }
    }
}
];

export const PRODUCEDIN1TB_MODULE_DECLARATIONS = [
    ProducedIn1TbHomeComponent,
    ProducedIn1TbNewComponent,
    ProducedIn1TbDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProducedIn1TbRoutingModule { }