import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFUSERADMIN-new',
  templateUrl: './WFUSERADMIN-new.component.html',
  styleUrls: ['./WFUSERADMIN-new.component.scss']
})
export class WFUSERADMINNewComponent {
  @ViewChild("WFUSERADMINForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'CreatedDate': '(getdate())'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}