import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFCompany-new',
  templateUrl: './WFCompany-new.component.html',
  styleUrls: ['./WFCompany-new.component.scss']
})
export class WFCompanyNewComponent {
  @ViewChild("WFCompanyForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'CompanyID': '0', 'CreatedDate': '(getdate())'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}