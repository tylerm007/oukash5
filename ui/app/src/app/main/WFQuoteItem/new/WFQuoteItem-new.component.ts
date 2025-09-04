import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFQuoteItem-new',
  templateUrl: './WFQuoteItem-new.component.html',
  styleUrls: ['./WFQuoteItem-new.component.scss']
})
export class WFQuoteItemNewComponent {
  @ViewChild("WFQuoteItemForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'SortOrder': '((1))', 'QuoteItemID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}