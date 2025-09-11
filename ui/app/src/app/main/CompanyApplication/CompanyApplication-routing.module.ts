import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CompanyApplicationHomeComponent } from './home/CompanyApplication-home.component';
import { CompanyApplicationNewComponent } from './new/CompanyApplication-new.component';
import { CompanyApplicationDetailComponent } from './detail/CompanyApplication-detail.component';

const routes: Routes = [
  {path: '', component: CompanyApplicationHomeComponent},
  { path: 'new', component: CompanyApplicationNewComponent },
  { path: ':ID', component: CompanyApplicationDetailComponent,
    data: {
      oPermission: {
        permissionId: 'CompanyApplication-detail-permissions'
      }
    }
  }
];

export const COMPANYAPPLICATION_MODULE_DECLARATIONS = [
    CompanyApplicationHomeComponent,
    CompanyApplicationNewComponent,
    CompanyApplicationDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class CompanyApplicationRoutingModule { }