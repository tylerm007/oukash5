import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'TaskCategory-new',
  templateUrl: './TaskCategory-new.component.html',
  styleUrls: ['./TaskCategory-new.component.scss']
})
export class TaskCategoryNewComponent {
  @ViewChild("TaskCategoryForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}