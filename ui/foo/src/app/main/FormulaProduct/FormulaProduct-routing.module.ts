import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { FormulaProductHomeComponent } from './home/FormulaProduct-home.component';
import { FormulaProductNewComponent } from './new/FormulaProduct-new.component';
import { FormulaProductDetailComponent } from './detail/FormulaProduct-detail.component';

const routes: Routes = [
  {path: '', component: FormulaProductHomeComponent},
  { path: 'new', component: FormulaProductNewComponent },
  { path: ':ID', component: FormulaProductDetailComponent,
    data: {
      oPermission: {
        permissionId: 'FormulaProduct-detail-permissions'
      }
    }
  }
];

export const FORMULAPRODUCT_MODULE_DECLARATIONS = [
    FormulaProductHomeComponent,
    FormulaProductNewComponent,
    FormulaProductDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class FormulaProductRoutingModule { }