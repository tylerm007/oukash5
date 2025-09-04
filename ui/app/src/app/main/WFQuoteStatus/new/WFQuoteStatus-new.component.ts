import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFQuoteStatus-new',
  templateUrl: './WFQuoteStatus-new.component.html',
  styleUrls: ['./WFQuoteStatus-new.component.scss']
})
export class WFQuoteStatusNewComponent {
  @ViewChild("WFQuoteStatusForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}