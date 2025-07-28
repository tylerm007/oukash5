import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'VISITSCOMMENT-new',
  templateUrl: './VISITSCOMMENT-new.component.html',
  styleUrls: ['./VISITSCOMMENT-new.component.scss']
})
export class VISITSCOMMENTNewComponent {
  @ViewChild("VISITSCOMMENTForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0', 'WHO': '(suser_sname())', 'ValidFromTime': '(sysutcdatetime())', 'ValidToTime': "(CONVERT([datetime2],'9999-12-31 23:59:59.9999999',(0)))"}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}