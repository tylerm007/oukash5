import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {YOSHONINFO_MODULE_DECLARATIONS, YoshonInfoRoutingModule} from  './YoshonInfo-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    YoshonInfoRoutingModule
  ],
  declarations: YOSHONINFO_MODULE_DECLARATIONS,
  exports: YOSHONINFO_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class YoshonInfoModule { }