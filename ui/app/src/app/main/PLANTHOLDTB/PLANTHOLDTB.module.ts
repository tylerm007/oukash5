import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PLANTHOLDTB_MODULE_DECLARATIONS, PLANTHOLDTBRoutingModule} from  './PLANTHOLDTB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    PLANTHOLDTBRoutingModule
  ],
  declarations: PLANTHOLDTB_MODULE_DECLARATIONS,
  exports: PLANTHOLDTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class PLANTHOLDTBModule { }