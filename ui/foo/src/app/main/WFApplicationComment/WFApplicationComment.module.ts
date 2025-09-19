import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {WFAPPLICATIONCOMMENT_MODULE_DECLARATIONS, WFApplicationCommentRoutingModule} from  './WFApplicationComment-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    WFApplicationCommentRoutingModule
  ],
  declarations: WFAPPLICATIONCOMMENT_MODULE_DECLARATIONS,
  exports: WFAPPLICATIONCOMMENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class WFApplicationCommentModule { }