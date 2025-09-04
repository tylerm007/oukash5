import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'StageInstance-new',
  templateUrl: './StageInstance-new.component.html',
  styleUrls: ['./StageInstance-new.component.scss']
})
export class StageInstanceNewComponent {
  @ViewChild("StageInstanceForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'StageInstanceId': '0', 'Status': "('NEW')", 'CreatedDate': '(getutcdate())', 'CreatedBy': "('System')"}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}