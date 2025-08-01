import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PRODUCTJOBLINEITEM_MODULE_DECLARATIONS, ProductJobLineItemRoutingModule} from  './ProductJobLineItem-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    ProductJobLineItemRoutingModule
  ],
  declarations: PRODUCTJOBLINEITEM_MODULE_DECLARATIONS,
  exports: PRODUCTJOBLINEITEM_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class ProductJobLineItemModule { }