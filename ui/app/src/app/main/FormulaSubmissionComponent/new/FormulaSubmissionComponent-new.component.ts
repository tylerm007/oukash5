import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'FormulaSubmissionComponent-new',
  templateUrl: './FormulaSubmissionComponent-new.component.html',
  styleUrls: ['./FormulaSubmissionComponent-new.component.scss']
})
export class FormulaSubmissionComponentNewComponent {
  @ViewChild("FormulaSubmissionComponentForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}