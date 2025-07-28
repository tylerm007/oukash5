import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'CompanyPlantOption-new',
  templateUrl: './CompanyPlantOption-new.component.html',
  styleUrls: ['./CompanyPlantOption-new.component.scss']
})
export class CompanyPlantOptionNewComponent {
  @ViewChild("CompanyPlantOptionForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ModifiedBy': '(suser_sname())', 'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))", 'ID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}