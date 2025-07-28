import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'COMPANYFEESTRUCTURE-new',
  templateUrl: './COMPANYFEESTRUCTURE-new.component.html',
  styleUrls: ['./COMPANYFEESTRUCTURE-new.component.scss']
})
export class COMPANYFEESTRUCTURENewComponent {
  @ViewChild("COMPANYFEESTRUCTUREForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))", 'COMPANY_FEE_ID': '((1))'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}