import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'PLANTTB-new',
  templateUrl: './PLANTTB-new.component.html',
  styleUrls: ['./PLANTTB-new.component.scss']
})
export class PLANTTBNewComponent {
  @ViewChild("PLANTTBForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'SPECIAL_PROD': 'N', 'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))", 'MaxOnSiteVisits': '0', 'MaxVirtualVisits': '0', 'IsDaily': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}