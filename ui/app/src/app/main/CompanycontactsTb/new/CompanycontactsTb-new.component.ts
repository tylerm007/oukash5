import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'CompanycontactsTb-new',
  templateUrl: './CompanycontactsTb-new.component.html',
  styleUrls: ['./CompanycontactsTb-new.component.scss']
})
export class CompanycontactsTbNewComponent {
  @ViewChild("CompanycontactsTbForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ccID': '0', 'PrimaryCT': "('N')", 'BillingCT': "('N')", 'WebCT': "('N')", 'OtherCT': "('N')", 'EnteredBy': '(suser_sname())', 'StatementType': "('N')", 'InvoiceType': "('N')", 'UsedInComment': "('')", 'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))", 'DateEntered': '(getdate())', 'UserVendorID': "('')", 'UsedByCompID': '((0))'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}