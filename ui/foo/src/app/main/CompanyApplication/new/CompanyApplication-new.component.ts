import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'CompanyApplication-new',
  templateUrl: './CompanyApplication-new.component.html',
  styleUrls: ['./CompanyApplication-new.component.scss']
})
export class CompanyApplicationNewComponent {
  @ViewChild("CompanyApplicationForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0', 'PreviousCertification': 'N', 'OUCertified': 'N', 'CurrentlyCertified': 'N', 'CompanyID': '0', 'dateSubmitted': 'getdate()'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}