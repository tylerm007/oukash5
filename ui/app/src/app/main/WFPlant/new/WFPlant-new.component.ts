import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFPlant-new',
  templateUrl: './WFPlant-new.component.html',
  styleUrls: ['./WFPlant-new.component.scss']
})
export class WFPlantNewComponent {
  @ViewChild("WFPlantForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'PlantID': '0', 'CreatedDate': '(getdate())'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}