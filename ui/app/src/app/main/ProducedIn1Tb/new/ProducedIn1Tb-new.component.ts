import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'ProducedIn1Tb-new',
  templateUrl: './ProducedIn1Tb-new.component.html',
  styleUrls: ['./ProducedIn1Tb-new.component.scss']
})
export class ProducedIn1TbNewComponent {
  @ViewChild("ProducedIn1TbForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'REGULAR': "('')", 'SPECIAL_STATUS_1': "('')", 'SPECIAL_STATUS_2': "('')", 'SPECIAL_STATUS_3': "('')", 'SPECIAL_STATUS_4': "('')", 'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))", 'ID': '0', 'PROC_LINE_ID': '((1))'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}