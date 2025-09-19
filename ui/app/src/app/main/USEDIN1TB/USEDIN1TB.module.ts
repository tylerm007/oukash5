import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {USEDIN1TB_MODULE_DECLARATIONS, USEDIN1TBRoutingModule} from  './USEDIN1TB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    USEDIN1TBRoutingModule
  ],
  declarations: USEDIN1TB_MODULE_DECLARATIONS,
  exports: USEDIN1TB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class USEDIN1TBModule { }