import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'AchStripePaymentDetail-new',
  templateUrl: './AchStripePaymentDetail-new.component.html',
  styleUrls: ['./AchStripePaymentDetail-new.component.scss']
})
export class AchStripePaymentDetailNewComponent {
  @ViewChild("AchStripePaymentDetailForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'Id': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}