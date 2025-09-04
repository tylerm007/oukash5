import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'TaskComment-new',
  templateUrl: './TaskComment-new.component.html',
  styleUrls: ['./TaskComment-new.component.scss']
})
export class TaskCommentNewComponent {
  @ViewChild("TaskCommentForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'CommentId': '0', 'CommentType': "('Internal')", 'CreatedDate': '(getutcdate())'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}