import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'RoleAssignment-new',
  templateUrl: './RoleAssignment-new.component.html',
  styleUrls: ['./RoleAssignment-new.component.scss']
})
export class RoleAssignmentNewComponent {
  @ViewChild("RoleAssignmentForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'RoleAssignmentID': '0', 'CreatedDate': '(getutcdate())', 'CreatedBy': "('System')"}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}