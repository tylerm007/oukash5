import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'OWNSTB-new',
  templateUrl: './OWNSTB-new.component.html',
  styleUrls: ['./OWNSTB-new.component.scss']
})
export class OWNSTBNewComponent {
  @ViewChild("OWNSTBForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0', 'NoRFRneeded': 'N', 'MoveToGP': 'N', 'ShareAB': 'N', 'AutoCertification': '0', 'Override': '0', 'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))", 'IsCertBillingOverride': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}