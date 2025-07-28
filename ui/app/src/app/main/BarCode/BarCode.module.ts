import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {BARCODE_MODULE_DECLARATIONS, BarCodeRoutingModule} from  './BarCode-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    BarCodeRoutingModule
  ],
  declarations: BARCODE_MODULE_DECLARATIONS,
  exports: BARCODE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class BarCodeModule { }