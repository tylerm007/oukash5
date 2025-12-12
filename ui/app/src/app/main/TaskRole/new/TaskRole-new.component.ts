import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'TaskRole-new',
  templateUrl: './TaskRole-new.component.html',
  styleUrls: ['./TaskRole-new.component.scss']
})
export class TaskRoleNewComponent {
  @ViewChild("TaskRoleForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}