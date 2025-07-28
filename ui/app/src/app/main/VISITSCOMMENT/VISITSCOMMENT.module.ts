import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {VISITSCOMMENT_MODULE_DECLARATIONS, VISITSCOMMENTRoutingModule} from  './VISITSCOMMENT-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    VISITSCOMMENTRoutingModule
  ],
  declarations: VISITSCOMMENT_MODULE_DECLARATIONS,
  exports: VISITSCOMMENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class VISITSCOMMENTModule { }