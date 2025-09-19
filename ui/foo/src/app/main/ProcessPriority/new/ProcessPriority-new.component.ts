import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'ProcessPriority-new',
  templateUrl: './ProcessPriority-new.component.html',
  styleUrls: ['./ProcessPriority-new.component.scss']
})
export class ProcessPriorityNewComponent {
  @ViewChild("ProcessPriorityForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}