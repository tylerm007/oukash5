import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFProduct-new',
  templateUrl: './WFProduct-new.component.html',
  styleUrls: ['./WFProduct-new.component.scss']
})
export class WFProductNewComponent {
  @ViewChild("WFProductForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'action': "('Add')", 'ProductID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}