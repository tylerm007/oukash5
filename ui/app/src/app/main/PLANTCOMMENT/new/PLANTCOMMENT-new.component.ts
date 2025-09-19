import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'PLANTCOMMENT-new',
  templateUrl: './PLANTCOMMENT-new.component.html',
  styleUrls: ['./PLANTCOMMENT-new.component.scss']
})
export class PLANTCOMMENTNewComponent {
  @ViewChild("PLANTCOMMENTForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}