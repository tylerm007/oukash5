import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFUserRole-new',
  templateUrl: './WFUserRole-new.component.html',
  styleUrls: ['./WFUserRole-new.component.scss']
})
export class WFUserRoleNewComponent {
  @ViewChild("WFUserRoleForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'CreatedDate': '(getdate())'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}