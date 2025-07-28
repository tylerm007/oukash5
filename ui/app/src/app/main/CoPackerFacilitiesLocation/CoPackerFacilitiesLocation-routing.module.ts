import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CoPackerFacilitiesLocationHomeComponent } from './home/CoPackerFacilitiesLocation-home.component';
import { CoPackerFacilitiesLocationNewComponent } from './new/CoPackerFacilitiesLocation-new.component';
import { CoPackerFacilitiesLocationDetailComponent } from './detail/CoPackerFacilitiesLocation-detail.component';

const routes: Routes = [
  {path: '', component: CoPackerFacilitiesLocationHomeComponent},
  { path: 'new', component: CoPackerFacilitiesLocationNewComponent },
  { path: ':ID', component: CoPackerFacilitiesLocationDetailComponent,
    data: {
      oPermission: {
        permissionId: 'CoPackerFacilitiesLocation-detail-permissions'
      }
    }
  }
];

export const COPACKERFACILITIESLOCATION_MODULE_DECLARATIONS = [
    CoPackerFacilitiesLocationHomeComponent,
    CoPackerFacilitiesLocationNewComponent,
    CoPackerFacilitiesLocationDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CoPackerFacilitiesLocationRoutingModule { }