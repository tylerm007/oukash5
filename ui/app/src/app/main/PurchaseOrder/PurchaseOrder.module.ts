import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PURCHASEORDER_MODULE_DECLARATIONS, PurchaseOrderRoutingModule} from  './PurchaseOrder-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PurchaseOrderRoutingModule
  ],
  declarations: PURCHASEORDER_MODULE_DECLARATIONS,
  exports: PURCHASEORDER_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PurchaseOrderModule { }