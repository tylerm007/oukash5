import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'COMPANYHOLDTB-new',
  templateUrl: './COMPANYHOLDTB-new.component.html',
  styleUrls: ['./COMPANYHOLDTB-new.component.scss']
})
export class COMPANYHOLDTBNewComponent {
  @ViewChild("COMPANYHOLDTBForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0', 'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}