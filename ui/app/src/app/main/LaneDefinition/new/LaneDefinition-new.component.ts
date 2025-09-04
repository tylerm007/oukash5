import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'LaneDefinition-new',
  templateUrl: './LaneDefinition-new.component.html',
  styleUrls: ['./LaneDefinition-new.component.scss']
})
export class LaneDefinitionNewComponent {
  @ViewChild("LaneDefinitionForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'LaneRole': "('NCRC')", 'CreatedDate': '(getutcdate())', 'LaneId': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}