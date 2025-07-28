import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'VISIT-new',
  templateUrl: './VISIT-new.component.html',
  styleUrls: ['./VISIT-new.component.scss']
})
export class VISITNewComponent {
  @ViewChild("VISITForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'VISIT_ID': '0', 'DESTINATION_TYPE': "('P')", 'VISIT_FOR_TYPE': "('C')", 'PERIOD_START_DATE': '(getdate())', 'ACTUAL_VISIT_DAYS': '((1))', 'DEFAULT_BILL_AMOUNT': '((0))', 'DEFAULT_EXPENSES': '((0))', 'DEFAULT_PAYMENT_AMOUNY': '((0))', 'OU_RENTAL_CAR': '((0))', 'OU_PLANE': '((0))', 'OU_OTHER': '((0))', 'OU_Mileage_Differential': '((0))', 'TOTAL_MASHGIACH_PAY': '((0))', 'TOTAL_MASHGIACH_EXPENSE': '((0))', 'TOTAL_MASHGIACH_ADVANCES': '((0))', 'TOTAL_BILLABLE_FEE': '((0))', 'TOTAL_BILLABLE_EXPENSES': '((0))', 'TOTAL_BILLABLE_PAYMENT': '((0))', 'PAY_TYPE': "('Per Visit')", 'PAY_AMOUNT': '((0))', 'PAY_OVERTIME': '((0))', 'PAY_OVERNIGHT': '((0))', 'NUMBER_SHIFTS': '((1))', 'PAY_TOTAL': '((0))', 'RATE_PER_MILEAGE': '((0))', 'BILLABLE_FEE': '((0))', 'BILLABLE_OVERTIME_FEE': '((0))', 'BILLABLE_OVERNIGHT_FEE': '((0))', 'VisitStatus': "('')", 'CreatedBy': '(suser_sname())', 'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))", 'TOTAL_EXPENSES_PAID': '((0))', 'MILEAGE_NOT_PAID': '((0))', 'PLANE_NOT_PAID': '((0))', 'RENTAL_CAR_NOT_PAID': '((0))', 'TOLLS_NOT_PAID': '((0))', 'PARKING_NOT_PAID': '((0))', 'GAS_NOT_PAID': '((0))', 'TAXI_NOT_PAID': '((0))', 'MOTEL_NOT_PAID': '((0))', 'TELEPHONE_NOT_PAID': '((0))', 'MISC_NOT_PAID': '((0))'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}