import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFDashboard-new',
  templateUrl: './WFDashboard-new.component.html',
  styleUrls: ['./WFDashboard-new.component.scss']
})
export class WFDashboardNewComponent {
  @ViewChild("WFDashboardForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'ID': '0', 'count_new': '((0))', 'count_in_progress': '((0))', 'count_withdrawn': '((0))', 'count_overdue': '((0))', 'total_count': '((0))', 'count_completed': '((0))'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}