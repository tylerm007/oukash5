import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'LabelBarcode-new',
  templateUrl: './LabelBarcode-new.component.html',
  styleUrls: ['./LabelBarcode-new.component.scss']
})
export class LabelBarcodeNewComponent {
  @ViewChild("LabelBarcodeForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}