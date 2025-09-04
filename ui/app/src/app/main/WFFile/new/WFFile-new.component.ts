import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFFile-new',
  templateUrl: './WFFile-new.component.html',
  styleUrls: ['./WFFile-new.component.scss']
})
export class WFFileNewComponent {
  @ViewChild("WFFileForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'CCreatedDate': '(getutcdate())', 'CreatedBy': "('System')", 'FileID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}