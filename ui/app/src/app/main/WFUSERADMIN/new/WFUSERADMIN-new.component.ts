import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFUserAdmin-new',
  templateUrl: './WFUserAdmin-new.component.html',
  styleUrls: ['./WFUserAdmin-new.component.scss']
})
export class WFUserAdminNewComponent {
  @ViewChild("WFUserAdminForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'CreatedDate': '(getdate())'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}