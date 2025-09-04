import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'LaneRole-new',
  templateUrl: './LaneRole-new.component.html',
  styleUrls: ['./LaneRole-new.component.scss']
})
export class LaneRoleNewComponent {
  @ViewChild("LaneRoleForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}