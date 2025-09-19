import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFApplicationComment-new',
  templateUrl: './WFApplicationComment-new.component.html',
  styleUrls: ['./WFApplicationComment-new.component.scss']
})
export class WFApplicationCommentNewComponent {
  @ViewChild("WFApplicationCommentForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'CommentType': 'internal', 'CreatedDate': 'getdate()'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}