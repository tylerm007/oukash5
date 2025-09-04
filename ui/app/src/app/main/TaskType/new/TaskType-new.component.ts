import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'TaskType-new',
  templateUrl: './TaskType-new.component.html',
  styleUrls: ['./TaskType-new.component.scss']
})
export class TaskTypeNewComponent {
  @ViewChild("TaskTypeForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}