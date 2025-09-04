import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'ProcessDefinition-new',
  templateUrl: './ProcessDefinition-new.component.html',
  styleUrls: ['./ProcessDefinition-new.component.scss']
})
export class ProcessDefinitionNewComponent {
  @ViewChild("ProcessDefinitionForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ProcessVersion': "('1.0')", 'CreatedDate': '(getutcdate())', 'ProcessId': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}