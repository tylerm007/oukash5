import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PLANTFEESTRUCTURE_MODULE_DECLARATIONS, PLANTFEESTRUCTURERoutingModule} from  './PLANTFEESTRUCTURE-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PLANTFEESTRUCTURERoutingModule
  ],
  declarations: PLANTFEESTRUCTURE_MODULE_DECLARATIONS,
  exports: PLANTFEESTRUCTURE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PLANTFEESTRUCTUREModule { }