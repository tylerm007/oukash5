import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ValidationRuleHomeComponent } from './home/ValidationRule-home.component';
import { ValidationRuleNewComponent } from './new/ValidationRule-new.component';
import { ValidationRuleDetailComponent } from './detail/ValidationRule-detail.component';

const routes: Routes = [
  {path: '', component: ValidationRuleHomeComponent},
  { path: 'new', component: ValidationRuleNewComponent },
  { path: ':ValidationId', component: ValidationRuleDetailComponent,
    data: {
      oPermission: {
        permissionId: 'ValidationRule-detail-permissions'
      }
    }
  },{
    path: ':ValidationId/ValidationResult', loadChildren: () => import('../ValidationResult/ValidationResult.module').then(m => m.ValidationResultModule),
    data: {
        oPermission: {
            permissionId: 'ValidationResult-detail-permissions'
        }
    }
}
];

export const VALIDATIONRULE_MODULE_DECLARATIONS = [
    ValidationRuleHomeComponent,
    ValidationRuleNewComponent,
    ValidationRuleDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ValidationRuleRoutingModule { }