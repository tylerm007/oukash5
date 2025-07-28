import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FormulaComponentHomeComponent } from './home/FormulaComponent-home.component';
import { FormulaComponentNewComponent } from './new/FormulaComponent-new.component';
import { FormulaComponentDetailComponent } from './detail/FormulaComponent-detail.component';

const routes: Routes = [
  {path: '', component: FormulaComponentHomeComponent},
  { path: 'new', component: FormulaComponentNewComponent },
  { path: ':ID', component: FormulaComponentDetailComponent,
    data: {
      oPermission: {
        permissionId: 'FormulaComponent-detail-permissions'
      }
    }
  }
];

export const FORMULACOMPONENT_MODULE_DECLARATIONS = [
    FormulaComponentHomeComponent,
    FormulaComponentNewComponent,
    FormulaComponentDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class FormulaComponentRoutingModule { }