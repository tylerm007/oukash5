import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'PLANTADDRESSTB-new',
  templateUrl: './PLANTADDRESSTB-new.component.html',
  styleUrls: ['./PLANTADDRESSTB-new.component.scss']
})
export class PLANTADDRESSTBNewComponent {
  @ViewChild("PLANTADDRESSTBForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0', 'STREET1': "('')", 'CITY': "('')", 'STATE': "('')", 'COUNTRY': "('')", 'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}