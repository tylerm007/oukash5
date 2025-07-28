import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CoPackerFacilityHomeComponent } from './home/CoPackerFacility-home.component';
import { CoPackerFacilityNewComponent } from './new/CoPackerFacility-new.component';
import { CoPackerFacilityDetailComponent } from './detail/CoPackerFacility-detail.component';

const routes: Routes = [
  {path: '', component: CoPackerFacilityHomeComponent},
  { path: 'new', component: CoPackerFacilityNewComponent },
  { path: ':ID', component: CoPackerFacilityDetailComponent,
    data: {
      oPermission: {
        permissionId: 'CoPackerFacility-detail-permissions'
      }
    }
  },{
    path: ':CoPackerId/CoPackerFacilitiesCategory', loadChildren: () => import('../CoPackerFacilitiesCategory/CoPackerFacilitiesCategory.module').then(m => m.CoPackerFacilitiesCategoryModule),
    data: {
        oPermission: {
            permissionId: 'CoPackerFacilitiesCategory-detail-permissions'
        }
    }
},{
    path: ':CoPackerId/CoPackerFacilitiesLocation', loadChildren: () => import('../CoPackerFacilitiesLocation/CoPackerFacilitiesLocation.module').then(m => m.CoPackerFacilitiesLocationModule),
    data: {
        oPermission: {
            permissionId: 'CoPackerFacilitiesLocation-detail-permissions'
        }
    }
}
];

export const COPACKERFACILITY_MODULE_DECLARATIONS = [
    CoPackerFacilityHomeComponent,
    CoPackerFacilityNewComponent,
    CoPackerFacilityDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CoPackerFacilityRoutingModule { }