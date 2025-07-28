import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FormulaSubmissionPlantHomeComponent } from './home/FormulaSubmissionPlant-home.component';
import { FormulaSubmissionPlantNewComponent } from './new/FormulaSubmissionPlant-new.component';
import { FormulaSubmissionPlantDetailComponent } from './detail/FormulaSubmissionPlant-detail.component';

const routes: Routes = [
  {path: '', component: FormulaSubmissionPlantHomeComponent},
  { path: 'new', component: FormulaSubmissionPlantNewComponent },
  { path: ':ID', component: FormulaSubmissionPlantDetailComponent,
    data: {
      oPermission: {
        permissionId: 'FormulaSubmissionPlant-detail-permissions'
      }
    }
  },{
    path: ':FormulaSubmissionPlantID/ProducedIn1Tb', loadChildren: () => import('../ProducedIn1Tb/ProducedIn1Tb.module').then(m => m.ProducedIn1TbModule),
    data: {
        oPermission: {
            permissionId: 'ProducedIn1Tb-detail-permissions'
        }
    }
}
];

export const FORMULASUBMISSIONPLANT_MODULE_DECLARATIONS = [
    FormulaSubmissionPlantHomeComponent,
    FormulaSubmissionPlantNewComponent,
    FormulaSubmissionPlantDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class FormulaSubmissionPlantRoutingModule { }