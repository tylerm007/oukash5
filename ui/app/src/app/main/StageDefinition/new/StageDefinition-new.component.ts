import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'StageDefinition-new',
  templateUrl: './StageDefinition-new.component.html',
  styleUrls: ['./StageDefinition-new.component.scss']
})
export class StageDefinitionNewComponent {
  @ViewChild("StageDefinitionForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'CreatedDate': '(getutcdate())', 'StageId': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}