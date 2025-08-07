import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'ASSIGNEDMASHGIACHTB-new',
  templateUrl: './ASSIGNEDMASHGIACHTB-new.component.html',
  styleUrls: ['./ASSIGNEDMASHGIACHTB-new.component.scss']
})
export class ASSIGNEDMASHGIACHTBNewComponent {
  @ViewChild("ASSIGNEDMASHGIACHTBForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0', 'SeasonalStart': '((1))', 'SeasonalEnd': '((12))'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}