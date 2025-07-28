import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'BarCode-new',
  templateUrl: './BarCode-new.component.html',
  styleUrls: ['./BarCode-new.component.scss']
})
export class BarCodeNewComponent {
  @ViewChild("BarCodeForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}