import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EventActionHomeComponent } from './home/EventAction-home.component';
import { EventActionNewComponent } from './new/EventAction-new.component';
import { EventActionDetailComponent } from './detail/EventAction-detail.component';

const routes: Routes = [
  {path: '', component: EventActionHomeComponent},
  { path: 'new', component: EventActionNewComponent },
  { path: ':EventId', component: EventActionDetailComponent,
    data: {
      oPermission: {
        permissionId: 'EventAction-detail-permissions'
      }
    }
  }
];

export const EVENTACTION_MODULE_DECLARATIONS = [
    EventActionHomeComponent,
    EventActionNewComponent,
    EventActionDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EventActionRoutingModule { }