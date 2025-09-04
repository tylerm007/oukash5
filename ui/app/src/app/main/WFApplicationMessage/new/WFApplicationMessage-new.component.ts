import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFApplicationMessage-new',
  templateUrl: './WFApplicationMessage-new.component.html',
  styleUrls: ['./WFApplicationMessage-new.component.scss']
})
export class WFApplicationMessageNewComponent {
  @ViewChild("WFApplicationMessageForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'MessageID': '0', 'MessageType': "('outgoing')", 'Priority': "('normal')", 'SentDate': '(getdate())'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}