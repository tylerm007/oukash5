import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {OWNSTB_MODULE_DECLARATIONS, OWNSTBRoutingModule} from  './OWNSTB-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    OWNSTBRoutingModule
  ],
  declarations: OWNSTB_MODULE_DECLARATIONS,
  exports: OWNSTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class OWNSTBModule { }