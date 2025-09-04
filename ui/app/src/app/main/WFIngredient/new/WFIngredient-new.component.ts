import { Component, Injector, ViewChild } from '@angular/core';
import { NavigationService, OFormComponent } from 'ontimize-web-ngx';

@Component({
  selector: 'WFIngredient-new',
  templateUrl: './WFIngredient-new.component.html',
  styleUrls: ['./WFIngredient-new.component.scss']
})
export class WFIngredientNewComponent {
  @ViewChild("WFIngredientForm") form: OFormComponent;
  onInsertMode() {
    const default_values = {'CreatedDate': '(getdate())', 'ModifiedDate': '(getdate())', 'IngredientID': '0'}
    this.form.setFieldValues(default_values);
  }
  constructor(protected injector: Injector) {
    this.injector.get(NavigationService).initialize();
  }
}