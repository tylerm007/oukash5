import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ValidationResultHomeComponent } from './home/ValidationResult-home.component';
import { ValidationResultNewComponent } from './new/ValidationResult-new.component';
import { ValidationResultDetailComponent } from './detail/ValidationResult-detail.component';

const routes: Routes = [
  {path: '', component: ValidationResultHomeComponent},
  { path: 'new', component: ValidationResultNewComponent },
  { path: ':ValidationResultId', component: ValidationResultDetailComponent,
    data: {
      oPermission: {
        permissionId: 'ValidationResult-detail-permissions'
      }
    }
  }
];

export const VALIDATIONRESULT_MODULE_DECLARATIONS = [
    ValidationResultHomeComponent,
    ValidationResultNewComponent,
    ValidationResultDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ValidationResultRoutingModule { }