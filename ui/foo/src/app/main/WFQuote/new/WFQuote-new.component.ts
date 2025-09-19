import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFQuote-new',
  templateUrl: './WFQuote-new.component.html',
  styleUrls: ['./WFQuote-new.component.scss']
})
export class WFQuoteNewComponent {
  @ViewChild("WFQuoteForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'Status': 'PEND', 'CreatedDate': 'getdate()'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}