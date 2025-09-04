import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'ValidationResult-new',
  templateUrl: './ValidationResult-new.component.html',
  styleUrls: ['./ValidationResult-new.component.scss']
})
export class ValidationResultNewComponent {
  @ViewChild("ValidationResultForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ValidationResultId': '0', 'ValidationDate': '(getutcdate())'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}