import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'StripeCustomer-new',
  templateUrl: './StripeCustomer-new.component.html',
  styleUrls: ['./StripeCustomer-new.component.scss']
})
export class StripeCustomerNewComponent {
  @ViewChild("StripeCustomerForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'Id': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}