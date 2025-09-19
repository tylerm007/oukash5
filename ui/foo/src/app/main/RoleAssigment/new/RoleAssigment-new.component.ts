import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'RoleAssigment-new',
  templateUrl: './RoleAssigment-new.component.html',
  styleUrls: ['./RoleAssigment-new.component.scss']
})
export class RoleAssigmentNewComponent {
  @ViewChild("RoleAssigmentForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'CreatedDate': 'getutcdate()', 'CreatedBy': 'System'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}