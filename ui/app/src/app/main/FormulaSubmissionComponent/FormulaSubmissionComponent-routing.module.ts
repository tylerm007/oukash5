import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FormulaSubmissionComponentHomeComponent } from './home/FormulaSubmissionComponent-home.component';
import { FormulaSubmissionComponentNewComponent } from './new/FormulaSubmissionComponent-new.component';
import { FormulaSubmissionComponentDetailComponent } from './detail/FormulaSubmissionComponent-detail.component';

const routes: Routes = [
  {path: '', component: FormulaSubmissionComponentHomeComponent},
  { path: 'new', component: FormulaSubmissionComponentNewComponent },
  { path: ':ID', component: FormulaSubmissionComponentDetailComponent,
    data: {
      oPermission: {
        permissionId: 'FormulaSubmissionComponent-detail-permissions'
      }
    }
  }
];

export const FORMULASUBMISSIONCOMPONENT_MODULE_DECLARATIONS = [
    FormulaSubmissionComponentHomeComponent,
    FormulaSubmissionComponentNewComponent,
    FormulaSubmissionComponentDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class FormulaSubmissionComponentRoutingModule { }