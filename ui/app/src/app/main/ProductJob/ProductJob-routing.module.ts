import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ProductJobHomeComponent } from './home/ProductJob-home.component';
import { ProductJobNewComponent } from './new/ProductJob-new.component';
import { ProductJobDetailComponent } from './detail/ProductJob-detail.component';

const routes: Routes = [
  {path: '', component: ProductJobHomeComponent},
  { path: 'new', component: ProductJobNewComponent },
  { path: ':ID', component: ProductJobDetailComponent,
    data: {
      oPermission: {
        permissionId: 'ProductJob-detail-permissions'
      }
    }
  }
];

export const PRODUCTJOB_MODULE_DECLARATIONS = [
    ProductJobHomeComponent,
    ProductJobNewComponent,
    ProductJobDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProductJobRoutingModule { }