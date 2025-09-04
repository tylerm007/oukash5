import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './ValidationResult-card.component.html',
  styleUrls: ['./ValidationResult-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.ValidationResult-card]': 'true'
  }
})

export class ValidationResultCardComponent {


}