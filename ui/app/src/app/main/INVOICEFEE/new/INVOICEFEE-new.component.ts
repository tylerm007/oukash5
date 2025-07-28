import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'INVOICEFEE-new',
  templateUrl: './INVOICEFEE-new.component.html',
  styleUrls: ['./INVOICEFEE-new.component.scss']
})
export class INVOICEFEENewComponent {
  @ViewChild("INVOICEFEEForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'PurchaseOrder': "('')", 'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))", 'BalanceInAccounting': '((0))', 'DeliveryMethod': "('')"}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}