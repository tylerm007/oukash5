import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'COMPANYFEECOMMENT-new',
  templateUrl: './COMPANYFEECOMMENT-new.component.html',
  styleUrls: ['./COMPANYFEECOMMENT-new.component.scss']
})
export class COMPANYFEECOMMENTNewComponent {
  @ViewChild("COMPANYFEECOMMENTForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}