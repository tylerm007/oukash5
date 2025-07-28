import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {LABELBARCODE_MODULE_DECLARATIONS, LabelBarcodeRoutingModule} from  './LabelBarcode-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    LabelBarcodeRoutingModule
  ],
  declarations: LABELBARCODE_MODULE_DECLARATIONS,
  exports: LABELBARCODE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class LabelBarcodeModule { }