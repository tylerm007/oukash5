import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'COMPANYCOMMENT-new',
  templateUrl: './COMPANYCOMMENT-new.component.html',
  styleUrls: ['./COMPANYCOMMENT-new.component.scss']
})
export class COMPANYCOMMENTNewComponent {
  @ViewChild("COMPANYCOMMENTForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}