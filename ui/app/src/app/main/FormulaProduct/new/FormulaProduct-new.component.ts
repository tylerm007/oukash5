import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'FormulaProduct-new',
  templateUrl: './FormulaProduct-new.component.html',
  styleUrls: ['./FormulaProduct-new.component.scss']
})
export class FormulaProductNewComponent {
  @ViewChild("FormulaProductForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}