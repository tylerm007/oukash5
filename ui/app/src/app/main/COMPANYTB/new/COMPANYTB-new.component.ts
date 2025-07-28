import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'COMPANYTB-new',
  templateUrl: './COMPANYTB-new.component.html',
  styleUrls: ['./COMPANYTB-new.component.scss']
})
export class COMPANYTBNewComponent {
  @ViewChild("COMPANYTBForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'LIST': "('Y')", 'GP_NOTIFY': '((0))', 'COMPANY_TYPE': "('')", 'INVOICE_TYPE': "('Company Summary')", 'MoveToGP': "('N')", 'DefaultPO': "('')", 'PrivateLabelPO': "('')", 'VisitPO': "('')", 'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))", 'COMPANY_ID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}