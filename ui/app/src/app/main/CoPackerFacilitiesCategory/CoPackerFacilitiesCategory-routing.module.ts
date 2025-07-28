import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CoPackerFacilitiesCategoryHomeComponent } from './home/CoPackerFacilitiesCategory-home.component';
import { CoPackerFacilitiesCategoryNewComponent } from './new/CoPackerFacilitiesCategory-new.component';
import { CoPackerFacilitiesCategoryDetailComponent } from './detail/CoPackerFacilitiesCategory-detail.component';

const routes: Routes = [
  {path: '', component: CoPackerFacilitiesCategoryHomeComponent},
  { path: 'new', component: CoPackerFacilitiesCategoryNewComponent },
  { path: ':ID', component: CoPackerFacilitiesCategoryDetailComponent,
    data: {
      oPermission: {
        permissionId: 'CoPackerFacilitiesCategory-detail-permissions'
      }
    }
  }
];

export const COPACKERFACILITIESCATEGORY_MODULE_DECLARATIONS = [
    CoPackerFacilitiesCategoryHomeComponent,
    CoPackerFacilitiesCategoryNewComponent,
    CoPackerFacilitiesCategoryDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CoPackerFacilitiesCategoryRoutingModule { }