import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'TaskCommentType-new',
  templateUrl: './TaskCommentType-new.component.html',
  styleUrls: ['./TaskCommentType-new.component.scss']
})
export class TaskCommentTypeNewComponent {
  @ViewChild("TaskCommentTypeForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}