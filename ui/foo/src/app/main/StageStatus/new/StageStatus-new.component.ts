import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'StageStatus-new',
  templateUrl: './StageStatus-new.component.html',
  styleUrls: ['./StageStatus-new.component.scss']
})
export class StageStatusNewComponent {
  @ViewChild("StageStatusForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}