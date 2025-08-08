import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'PLANTSTATUSTB-new',
  templateUrl: './PLANTSTATUSTB-new.component.html',
  styleUrls: ['./PLANTSTATUSTB-new.component.scss']
})
export class PLANTSTATUSTBNewComponent {
  @ViewChild("PLANTSTATUSTBForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0', 'OwnsID': '((0))', 'DateDone': '(getdate())', 'ValidFromTime': "(CONVERT([datetime2](7),'1900-01-01 00:00:00'))", 'ValidToTime': "(CONVERT([datetime2](7),'9999-12-31 23:59:59.9999999'))", 'START_PERSON_ID': "('')"}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}