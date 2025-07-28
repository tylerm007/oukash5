import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { INVOICEFEEHomeComponent } from './home/INVOICEFEE-home.component';
import { INVOICEFEENewComponent } from './new/INVOICEFEE-new.component';
import { INVOICEFEEDetailComponent } from './detail/INVOICEFEE-detail.component';

const routes: Routes = [
  {path: '', component: INVOICEFEEHomeComponent},
  { path: 'new', component: INVOICEFEENewComponent },
  { path: ':INVOICE_ID', component: INVOICEFEEDetailComponent,
    data: {
      oPermission: {
        permissionId: 'INVOICEFEE-detail-permissions'
      }
    }
  }
];

export const INVOICEFEE_MODULE_DECLARATIONS = [
    INVOICEFEEHomeComponent,
    INVOICEFEENewComponent,
    INVOICEFEEDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class INVOICEFEERoutingModule { }