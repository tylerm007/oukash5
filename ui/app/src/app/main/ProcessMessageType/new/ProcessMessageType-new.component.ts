import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'ProcessMessageType-new',
  templateUrl: './ProcessMessageType-new.component.html',
  styleUrls: ['./ProcessMessageType-new.component.scss']
})
export class ProcessMessageTypeNewComponent {
  @ViewChild("ProcessMessageTypeForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}