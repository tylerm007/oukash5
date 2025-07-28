import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {MERCHCOMMENT_MODULE_DECLARATIONS, MERCHCOMMENTRoutingModule} from  './MERCHCOMMENT-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    MERCHCOMMENTRoutingModule
  ],
  declarations: MERCHCOMMENT_MODULE_DECLARATIONS,
  exports: MERCHCOMMENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class MERCHCOMMENTModule { }