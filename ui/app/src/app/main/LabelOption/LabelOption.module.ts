import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {LABELOPTION_MODULE_DECLARATIONS, LabelOptionRoutingModule} from  './LabelOption-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    LabelOptionRoutingModule
  ],
  declarations: LABELOPTION_MODULE_DECLARATIONS,
  exports: LABELOPTION_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class LabelOptionModule { }