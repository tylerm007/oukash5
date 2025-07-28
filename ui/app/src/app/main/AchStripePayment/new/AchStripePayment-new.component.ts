import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'AchStripePayment-new',
  templateUrl: './AchStripePayment-new.component.html',
  styleUrls: ['./AchStripePayment-new.component.scss']
})
export class AchStripePaymentNewComponent {
  @ViewChild("AchStripePaymentForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'FeeAmount': '((0))', 'Id': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}