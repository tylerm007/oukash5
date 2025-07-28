import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'PERSONJOBSTATUSTB-new',
  templateUrl: './PERSONJOBSTATUSTB-new.component.html',
  styleUrls: ['./PERSONJOBSTATUSTB-new.component.scss']
})
export class PERSONJOBSTATUSTBNewComponent {
  @ViewChild("PERSONJOBSTATUSTBForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}