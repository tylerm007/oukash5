import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'MERCHTB-new',
  templateUrl: './MERCHTB-new.component.html',
  styleUrls: ['./MERCHTB-new.component.scss']
})
export class MERCHTBNewComponent {
  @ViewChild("MERCHTBForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'STIPULATION': "('')", 'CONFIDENTIAL': "('N')", 'INSTITUTIONAL': "('N')", 'PESACH': "('N')", 'LOC_CATEGORY': "('')", 'PROD_NUM': "('')", 'INTERMEDIATE_MIX': "('N')", 'BrochoCode': '((0))', 'Brocho2Code': '((0))', 'CAS': "('')", 'Symbol': "('')", 'UKDdisplay': "('Y')", 'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))", 'MERCHANDISE_ID': '0', 'AS_STIPULATED': "('N')", 'OUP_REQUIRED': "('N')"}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}