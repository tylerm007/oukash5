import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WFIngredientHomeComponent } from './home/WFIngredient-home.component';
import { WFIngredientNewComponent } from './new/WFIngredient-new.component';
import { WFIngredientDetailComponent } from './detail/WFIngredient-detail.component';

const routes: Routes = [
  {path: '', component: WFIngredientHomeComponent},
  { path: 'new', component: WFIngredientNewComponent },
  { path: ':IngredientID', component: WFIngredientDetailComponent,
    data: {
      oPermission: {
        permissionId: 'WFIngredient-detail-permissions'
      }
    }
  }
];

export const WFINGREDIENT_MODULE_DECLARATIONS = [
    WFIngredientHomeComponent,
    WFIngredientNewComponent,
    WFIngredientDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WFIngredientRoutingModule { }