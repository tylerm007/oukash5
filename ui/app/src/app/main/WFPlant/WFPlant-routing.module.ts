import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFPlantHomeComponent } from './home/WFPlant-home.component';
import { WFPlantNewComponent } from './new/WFPlant-new.component';
import { WFPlantDetailComponent } from './detail/WFPlant-detail.component';

const routes: Routes = [
  {path: '', component: WFPlantHomeComponent},
  { path: 'new', component: WFPlantNewComponent },
  { path: ':PlantID', component: WFPlantDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFPlant-detail-permissions'
      }
    }
  }
];

export const WFPLANT_MODULE_DECLARATIONS = [
    WFPlantHomeComponent,
    WFPlantNewComponent,
    WFPlantDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFPlantRoutingModule { }