import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'FormulaSubmissionPlant-new',
  templateUrl: './FormulaSubmissionPlant-new.component.html',
  styleUrls: ['./FormulaSubmissionPlant-new.component.scss']
})
export class FormulaSubmissionPlantNewComponent {
  @ViewChild("FormulaSubmissionPlantForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}