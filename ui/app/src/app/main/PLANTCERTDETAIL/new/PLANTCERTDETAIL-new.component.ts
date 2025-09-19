import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'PLANTCERTDETAIL-new',
  templateUrl: './PLANTCERTDETAIL-new.component.html',
  styleUrls: ['./PLANTCERTDETAIL-new.component.scss']
})
export class PLANTCERTDETAILNewComponent {
  @ViewChild("PLANTCERTDETAILForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}