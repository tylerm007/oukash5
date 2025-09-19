import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFPriority-new',
  templateUrl: './WFPriority-new.component.html',
  styleUrls: ['./WFPriority-new.component.scss']
})
export class WFPriorityNewComponent {
  @ViewChild("WFPriorityForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}