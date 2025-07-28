import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'PLANTFEECOMMENT-new',
  templateUrl: './PLANTFEECOMMENT-new.component.html',
  styleUrls: ['./PLANTFEECOMMENT-new.component.scss']
})
export class PLANTFEECOMMENTNewComponent {
  @ViewChild("PLANTFEECOMMENTForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}