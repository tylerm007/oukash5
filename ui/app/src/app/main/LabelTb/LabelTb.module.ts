import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {LABELTB_MODULE_DECLARATIONS, LabelTbRoutingModule} from  './LabelTb-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    LabelTbRoutingModule
  ],
  declarations: LABELTB_MODULE_DECLARATIONS,
  exports: LABELTB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class LabelTbModule { }