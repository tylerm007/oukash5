import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'LabelOption-new',
  templateUrl: './LabelOption-new.component.html',
  styleUrls: ['./LabelOption-new.component.scss']
})
export class LabelOptionNewComponent {
  @ViewChild("LabelOptionForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}