import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFUSERROLE-new',
  templateUrl: './WFUSERROLE-new.component.html',
  styleUrls: ['./WFUSERROLE-new.component.scss']
})
export class WFUSERROLENewComponent {
  @ViewChild("WFUSERROLEForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'CreatedDate': '(getdate())'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}