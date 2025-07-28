import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'PERSONTB-new',
  templateUrl: './PERSONTB-new.component.html',
  styleUrls: ['./PERSONTB-new.component.scss']
})
export class PERSONTBNewComponent {
  @ViewChild("PERSONTBForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'PERSON_ID': '0', 'MIDDLE': "('')", 'PREFIX': "('')", 'SENDTICKETTO': "('')", 'MaxPay': '((500))', 'HiddenSSN': '((0))', 'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))"}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}