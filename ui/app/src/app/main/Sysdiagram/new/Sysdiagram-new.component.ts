import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'Sysdiagram-new',
  templateUrl: './Sysdiagram-new.component.html',
  styleUrls: ['./Sysdiagram-new.component.scss']
})
export class SysdiagramNewComponent {
  @ViewChild("SysdiagramForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'diagram_id': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}