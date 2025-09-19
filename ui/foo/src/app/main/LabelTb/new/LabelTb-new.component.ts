import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'LabelTb-new',
  templateUrl: './LabelTb-new.component.html',
  styleUrls: ['./LabelTb-new.component.scss']
})
export class LabelTbNewComponent {
  @ViewChild("LabelTbForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0', 'SEAL_SIGN': "('{NONE}')", 'GRP': '3', 'CREATE_DATE': 'getdate()', 'LAST_MODIFY_DATE': 'getdate()', 'CREATED_BY': 'suser_sname()', 'MODIFIED_BY': 'suser_sname()', 'PassoverSpecialProduction': 'N', 'DisplayNewlyCertifiedOnWeb': 'N', 'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))", 'IsDairyEquipment': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}