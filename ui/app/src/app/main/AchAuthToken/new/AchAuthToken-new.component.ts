import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'AchAuthToken-new',
  templateUrl: './AchAuthToken-new.component.html',
  styleUrls: ['./AchAuthToken-new.component.scss']
})
export class AchAuthTokenNewComponent {
  @ViewChild("AchAuthTokenForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'Id': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}