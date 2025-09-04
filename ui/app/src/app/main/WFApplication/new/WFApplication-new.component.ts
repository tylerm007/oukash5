import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFApplication-new',
  templateUrl: './WFApplication-new.component.html',
  styleUrls: ['./WFApplication-new.component.scss']
})
export class WFApplicationNewComponent {
  @ViewChild("WFApplicationForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ApplicationID': '0', 'Priority': "('NORMAL')", 'Status': "('NEW')", 'WFDashboardID': '((1))', 'CreatedDate': '(getutcdate())', 'CreatedBy': "('System')"}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}