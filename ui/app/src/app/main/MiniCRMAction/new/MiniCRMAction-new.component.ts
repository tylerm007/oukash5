import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'MiniCRMAction-new',
  templateUrl: './MiniCRMAction-new.component.html',
  styleUrls: ['./MiniCRMAction-new.component.scss']
})
export class MiniCRMActionNewComponent {
  @ViewChild("MiniCRMActionForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}