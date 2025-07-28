import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'AchPlaidLambdaResponse-new',
  templateUrl: './AchPlaidLambdaResponse-new.component.html',
  styleUrls: ['./AchPlaidLambdaResponse-new.component.scss']
})
export class AchPlaidLambdaResponseNewComponent {
  @ViewChild("AchPlaidLambdaResponseForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'Id': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}