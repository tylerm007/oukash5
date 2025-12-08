import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'EventAction-new',
  templateUrl: './EventAction-new.component.html',
  styleUrls: ['./EventAction-new.component.scss']
})
export class EventActionNewComponent {
  @ViewChild("EventActionForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'EventId': '0', 'EventStatus': "('PENDING')", 'EventType': "('External')", 'StartDate': '(getutcdate())'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}