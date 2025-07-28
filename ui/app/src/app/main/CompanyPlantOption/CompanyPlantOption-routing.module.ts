import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CompanyPlantOptionHomeComponent } from './home/CompanyPlantOption-home.component';
import { CompanyPlantOptionNewComponent } from './new/CompanyPlantOption-new.component';
import { CompanyPlantOptionDetailComponent } from './detail/CompanyPlantOption-detail.component';

const routes: Routes = [
  {path: '', component: CompanyPlantOptionHomeComponent},
  { path: 'new', component: CompanyPlantOptionNewComponent },
  { path: ':ID', component: CompanyPlantOptionDetailComponent,
    data: {
      oPermission: {
        permissionId: 'CompanyPlantOption-detail-permissions'
      }
    }
  }
];

export const COMPANYPLANTOPTION_MODULE_DECLARATIONS = [
    CompanyPlantOptionHomeComponent,
    CompanyPlantOptionNewComponent,
    CompanyPlantOptionDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CompanyPlantOptionRoutingModule { }