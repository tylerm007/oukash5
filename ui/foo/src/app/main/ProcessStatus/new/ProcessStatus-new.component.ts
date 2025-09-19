import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'ProcessStatus-new',
  templateUrl: './ProcessStatus-new.component.html',
  styleUrls: ['./ProcessStatus-new.component.scss']
})
export class ProcessStatusNewComponent {
  @ViewChild("ProcessStatusForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}