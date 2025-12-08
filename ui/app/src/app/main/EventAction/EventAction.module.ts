import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {EVENTACTION_MODULE_DECLARATIONS, EventActionRoutingModule} from  './EventAction-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    EventActionRoutingModule
  ],
  declarations: EVENTACTION_MODULE_DECLARATIONS,
  exports: EVENTACTION_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class EventActionModule { }