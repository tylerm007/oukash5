import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'ValidationRule-new',
  templateUrl: './ValidationRule-new.component.html',
  styleUrls: ['./ValidationRule-new.component.scss']
})
export class ValidationRuleNewComponent {
  @ViewChild("ValidationRuleForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'CreatedDate': '(getutcdate())', 'ValidationId': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}