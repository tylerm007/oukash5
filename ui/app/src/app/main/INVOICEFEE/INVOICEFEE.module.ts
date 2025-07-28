import {CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { OntimizeWebModule } from 'ontimize-web-ngx';
import { SharedModule } from '../../shared/shared.module';
import  {INVOICEFEE_MODULE_DECLARATIONS, INVOICEFEERoutingModule} from  './INVOICEFEE-routing.module';

@NgModule({

  imports: [
    SharedModule,
    CommonModule,
    OntimizeWebModule,
    INVOICEFEERoutingModule
  ],
  declarations: INVOICEFEE_MODULE_DECLARATIONS,
  exports: INVOICEFEE_MODULE_DECLARATIONS,
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class INVOICEFEEModule { }