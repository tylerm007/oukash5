import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFActivityLog-new',
  templateUrl: './WFActivityLog-new.component.html',
  styleUrls: ['./WFActivityLog-new.component.scss']
})
export class WFActivityLogNewComponent {
  @ViewChild("WFActivityLogForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'Status': "('APP')", 'ActivityDate': '(getdate())', 'ActivityID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}