import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {LABELCOMMENT_MODULE_DECLARATIONS, LabelCommentRoutingModule} from  './LabelComment-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    LabelCommentRoutingModule
  ],
  declarations: LABELCOMMENT_MODULE_DECLARATIONS,
  exports: LABELCOMMENT_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class LabelCommentModule { }