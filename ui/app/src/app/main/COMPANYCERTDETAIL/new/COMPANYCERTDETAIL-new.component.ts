import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'COMPANYCERTDETAIL-new',
  templateUrl: './COMPANYCERTDETAIL-new.component.html',
  styleUrls: ['./COMPANYCERTDETAIL-new.component.scss']
})
export class COMPANYCERTDETAILNewComponent {
  @ViewChild("COMPANYCERTDETAILForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}