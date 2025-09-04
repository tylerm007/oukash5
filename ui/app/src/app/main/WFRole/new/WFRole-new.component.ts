import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFRole-new',
  templateUrl: './WFRole-new.component.html',
  styleUrls: ['./WFRole-new.component.scss']
})
export class WFRoleNewComponent {
  @ViewChild("WFRoleForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'CreatedDate': '(getdate())'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}