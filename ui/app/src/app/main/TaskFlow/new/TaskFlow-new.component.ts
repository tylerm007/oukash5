import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'TaskFlow-new',
  templateUrl: './TaskFlow-new.component.html',
  styleUrls: ['./TaskFlow-new.component.scss']
})
export class TaskFlowNewComponent {
  @ViewChild("TaskFlowForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'FlowId': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}