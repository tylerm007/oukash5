import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './ValidationRule-card.component.html',
  styleUrls: ['./ValidationRule-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.ValidationRule-card]': 'true'
  }
})

export class ValidationRuleCardComponent {


}