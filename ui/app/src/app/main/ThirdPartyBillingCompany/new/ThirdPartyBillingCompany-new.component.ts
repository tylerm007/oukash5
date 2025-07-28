import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'ThirdPartyBillingCompany-new',
  templateUrl: './ThirdPartyBillingCompany-new.component.html',
  styleUrls: ['./ThirdPartyBillingCompany-new.component.scss']
})
export class ThirdPartyBillingCompanyNewComponent {
  @ViewChild("ThirdPartyBillingCompanyForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}