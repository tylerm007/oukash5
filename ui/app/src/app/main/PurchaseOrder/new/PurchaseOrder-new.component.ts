import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'PurchaseOrder-new',
  templateUrl: './PurchaseOrder-new.component.html',
  styleUrls: ['./PurchaseOrder-new.component.scss']
})
export class PurchaseOrderNewComponent {
  @ViewChild("PurchaseOrderForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}