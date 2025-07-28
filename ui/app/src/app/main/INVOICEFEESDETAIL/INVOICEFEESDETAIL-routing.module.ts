import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { INVOICEFEESDETAILHomeComponent } from './home/INVOICEFEESDETAIL-home.component';
import { INVOICEFEESDETAILNewComponent } from './new/INVOICEFEESDETAIL-new.component';
import { INVOICEFEESDETAILDetailComponent } from './detail/INVOICEFEESDETAIL-detail.component';

const routes: Routes = [
  {path: '', component: INVOICEFEESDETAILHomeComponent},
  { path: 'new', component: INVOICEFEESDETAILNewComponent },
  { path: ':ID', component: INVOICEFEESDETAILDetailComponent,
    data: {
      oPermission: {
        permissionId: 'INVOICEFEESDETAIL-detail-permissions'
      }
    }
  }
];

export const INVOICEFEESDETAIL_MODULE_DECLARATIONS = [
    INVOICEFEESDETAILHomeComponent,
    INVOICEFEESDETAILNewComponent,
    INVOICEFEESDETAILDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class INVOICEFEESDETAILRoutingModule { }