import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'USEDIN1TB-new',
  templateUrl: './USEDIN1TB-new.component.html',
  styleUrls: ['./USEDIN1TB-new.component.scss']
})
export class USEDIN1TBNewComponent {
  @ViewChild("USEDIN1TBForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'BrokerID': '((0))', 'START_DATE': '(getdate())', 'COMMENT': "('')", 'RAW_MATERIAL_CODE': "('')", 'ENTERED_BY': '(suser_sname())', 'DoNotDelete': "('N')", 'PassoverProductionUse': "('Non Passover')", 'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))", 'ID': '0', 'PreferredBrokerContactID': '((0))', 'PreferredSourceContactID': '((0))'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}