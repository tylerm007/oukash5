import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'COMPANYOTHERNAME-new',
  templateUrl: './COMPANYOTHERNAME-new.component.html',
  styleUrls: ['./COMPANYOTHERNAME-new.component.scss']
})
export class COMPANYOTHERNAMENewComponent {
  @ViewChild("COMPANYOTHERNAMEForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}