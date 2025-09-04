import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'ProcessMessage-new',
  templateUrl: './ProcessMessage-new.component.html',
  styleUrls: ['./ProcessMessage-new.component.scss']
})
export class ProcessMessageNewComponent {
  @ViewChild("ProcessMessageForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'MessageId': '0', 'MessageType': "('Standard')", 'SentDate': '(getutcdate())'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}