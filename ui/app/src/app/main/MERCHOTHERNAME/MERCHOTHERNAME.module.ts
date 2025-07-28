import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {MERCHOTHERNAME_MODULE_DECLARATIONS, MERCHOTHERNAMERoutingModule} from  './MERCHOTHERNAME-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    MERCHOTHERNAMERoutingModule
  ],
  declarations: MERCHOTHERNAME_MODULE_DECLARATIONS,
  exports: MERCHOTHERNAME_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class MERCHOTHERNAMEModule { }