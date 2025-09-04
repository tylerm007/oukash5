import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFContact-new',
  templateUrl: './WFContact-new.component.html',
  styleUrls: ['./WFContact-new.component.scss']
})
export class WFContactNewComponent {
  @ViewChild("WFContactForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ContactID': '0', 'CreatedDate': '(getdate())'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}