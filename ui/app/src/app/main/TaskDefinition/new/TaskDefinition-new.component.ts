import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'TaskDefinition-new',
  templateUrl: './TaskDefinition-new.component.html',
  styleUrls: ['./TaskDefinition-new.component.scss']
})
export class TaskDefinitionNewComponent {
  @ViewChild("TaskDefinitionForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'TaskId': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}