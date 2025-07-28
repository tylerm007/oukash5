import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PRODUCTJOB_MODULE_DECLARATIONS, ProductJobRoutingModule} from  './ProductJob-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    ProductJobRoutingModule
  ],
  declarations: PRODUCTJOB_MODULE_DECLARATIONS,
  exports: PRODUCTJOB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class ProductJobModule { }