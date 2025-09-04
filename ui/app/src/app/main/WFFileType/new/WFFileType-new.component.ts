import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFFileType-new',
  templateUrl: './WFFileType-new.component.html',
  styleUrls: ['./WFFileType-new.component.scss']
})
export class WFFileTypeNewComponent {
  @ViewChild("WFFileTypeForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}