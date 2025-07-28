import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'YoshonInfo-new',
  templateUrl: './YoshonInfo-new.component.html',
  styleUrls: ['./YoshonInfo-new.component.scss']
})
export class YoshonInfoNewComponent {
  @ViewChild("YoshonInfoForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ValidFromTime': '(sysutcdatetime())', 'ValidToTime': "(CONVERT([datetime2],'9999-12-31 23:59:59.9999999'))", 'Id': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}