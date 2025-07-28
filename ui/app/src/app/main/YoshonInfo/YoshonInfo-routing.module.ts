import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { YoshonInfoHomeComponent } from './home/YoshonInfo-home.component';
import { YoshonInfoNewComponent } from './new/YoshonInfo-new.component';
import { YoshonInfoDetailComponent } from './detail/YoshonInfo-detail.component';

const routes: Routes = [
  {path: '', component: YoshonInfoHomeComponent},
  { path: 'new', component: YoshonInfoNewComponent },
  { path: ':Id', component: YoshonInfoDetailComponent,
    data: {
      oPermission: {
        permissionId: 'YoshonInfo-detail-permissions'
      }
    }
  }
];

export const YOSHONINFO_MODULE_DECLARATIONS = [
    YoshonInfoHomeComponent,
    YoshonInfoNewComponent,
    YoshonInfoDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class YoshonInfoRoutingModule { }