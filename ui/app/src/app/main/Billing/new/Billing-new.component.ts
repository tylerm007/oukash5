import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'Billing-new',
  templateUrl: './Billing-new.component.html',
  styleUrls: ['./Billing-new.component.scss']
})
export class BillingNewComponent {
  @ViewChild("BillingForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'Id': '0', 'Amount': '((0))', 'VirtualAmount': '((0))'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}