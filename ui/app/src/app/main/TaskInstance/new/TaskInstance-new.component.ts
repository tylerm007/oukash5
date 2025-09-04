import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'TaskInstance-new',
  templateUrl: './TaskInstance-new.component.html',
  styleUrls: ['./TaskInstance-new.component.scss']
})
export class TaskInstanceNewComponent {
  @ViewChild("TaskInstanceForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'TaskInstanceId': '0', 'Status': "('Pending')", 'RetryCount': '((0))'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}