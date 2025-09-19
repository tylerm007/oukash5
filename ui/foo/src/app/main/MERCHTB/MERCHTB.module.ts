import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {MERCHTB_MODULE_DECLARATIONS, MERCHTBRoutingModule} from  './MERCHTB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    MERCHTBRoutingModule
  ],
  declarations: MERCHTB_MODULE_DECLARATIONS,
  exports: MERCHTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class MERCHTBModule { }