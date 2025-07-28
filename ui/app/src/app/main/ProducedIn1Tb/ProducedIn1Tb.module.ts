import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {PRODUCEDIN1TB_MODULE_DECLARATIONS, ProducedIn1TbRoutingModule} from  './ProducedIn1Tb-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    ProducedIn1TbRoutingModule
  ],
  declarations: PRODUCEDIN1TB_MODULE_DECLARATIONS,
  exports: PRODUCEDIN1TB_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class ProducedIn1TbModule { }