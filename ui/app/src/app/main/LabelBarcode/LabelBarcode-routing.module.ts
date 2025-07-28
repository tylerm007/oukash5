import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LabelBarcodeHomeComponent } from './home/LabelBarcode-home.component';
import { LabelBarcodeNewComponent } from './new/LabelBarcode-new.component';
import { LabelBarcodeDetailComponent } from './detail/LabelBarcode-detail.component';

const routes: Routes = [
  {path: '', component: LabelBarcodeHomeComponent},
  { path: 'new', component: LabelBarcodeNewComponent },
  { path: ':labelId/:barcodeId', component: LabelBarcodeDetailComponent,
    data: {
      oPermission: {
        permissionId: 'LabelBarcode-detail-permissions'
      }
    }
  }
];

export const LABELBARCODE_MODULE_DECLARATIONS = [
    LabelBarcodeHomeComponent,
    LabelBarcodeNewComponent,
    LabelBarcodeDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class LabelBarcodeRoutingModule { }