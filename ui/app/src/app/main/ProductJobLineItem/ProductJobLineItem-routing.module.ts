import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProductJobLineItemHomeComponent } from './home/ProductJobLineItem-home.component';
import { ProductJobLineItemNewComponent } from './new/ProductJobLineItem-new.component';
import { ProductJobLineItemDetailComponent } from './detail/ProductJobLineItem-detail.component';

const routes: Routes = [
  {path: '', component: ProductJobLineItemHomeComponent},
  { path: 'new', component: ProductJobLineItemNewComponent },
  { path: ':ID', component: ProductJobLineItemDetailComponent,
    data: {
      oPermission: {
        permissionId: 'ProductJobLineItem-detail-permissions'
      }
    }
  }
];

export const PRODUCTJOBLINEITEM_MODULE_DECLARATIONS = [
    ProductJobLineItemHomeComponent,
    ProductJobLineItemNewComponent,
    ProductJobLineItemDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProductJobLineItemRoutingModule { }