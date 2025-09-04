import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WorkflowHistory-new',
  templateUrl: './WorkflowHistory-new.component.html',
  styleUrls: ['./WorkflowHistory-new.component.scss']
})
export class WorkflowHistoryNewComponent {
  @ViewChild("WorkflowHistoryForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'HistoryId': '0', 'ActionDate': '(getutcdate())'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}