import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PLANTTB_MODULE_DECLARATIONS, PLANTTBRoutingModule} from  './PLANTTB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PLANTTBRoutingModule
  ],
  declarations: PLANTTB_MODULE_DECLARATIONS,
  exports: PLANTTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PLANTTBModule { }