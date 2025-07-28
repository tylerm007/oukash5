import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'PLANTFEESTRUCTURE-new',
  templateUrl: './PLANTFEESTRUCTURE-new.component.html',
  styleUrls: ['./PLANTFEESTRUCTURE-new.component.scss']
})
export class PLANTFEESTRUCTURENewComponent {
  @ViewChild("PLANTFEESTRUCTUREForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'APPROVAL': '((0))', 'IN_BILL_PASSOVER_TYPEx': "('Percent')", 'IN_BILL_PASSOVER_AMTx': '((100))', 'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))", 'COMPANY_FEE_ID': '((1))'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}