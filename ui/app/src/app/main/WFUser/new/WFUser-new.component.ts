import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFUser-new',
  templateUrl: './WFUser-new.component.html',
  styleUrls: ['./WFUser-new.component.scss']
})
export class WFUserNewComponent {
  @ViewChild("WFUserForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'Role': "('ADMIN')", 'CreatedDate': '(getdate())', 'UserID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}