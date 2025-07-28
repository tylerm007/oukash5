import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'PrivateLabelTemplate-new',
  templateUrl: './PrivateLabelTemplate-new.component.html',
  styleUrls: ['./PrivateLabelTemplate-new.component.scss']
})
export class PrivateLabelTemplateNewComponent {
  @ViewChild("PrivateLabelTemplateForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}