import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { BarCodeHomeComponent } from './home/BarCode-home.component';
import { BarCodeNewComponent } from './new/BarCode-new.component';
import { BarCodeDetailComponent } from './detail/BarCode-detail.component';

const routes: Routes = [
  {path: '', component: BarCodeHomeComponent},
  { path: 'new', component: BarCodeNewComponent },
  { path: ':Id', component: BarCodeDetailComponent,
    data: {
      oPermission: {
        permissionId: 'BarCode-detail-permissions'
      }
    }
  },{
    path: ':barcodeId/LabelBarcode', loadChildren: () => import('../LabelBarcode/LabelBarcode.module').then(m => m.LabelBarcodeModule),
    data: {
        oPermission: {
            permissionId: 'LabelBarcode-detail-permissions'
        }
    }
}
];

export const BARCODE_MODULE_DECLARATIONS = [
    BarCodeHomeComponent,
    BarCodeNewComponent,
    BarCodeDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class BarCodeRoutingModule { }