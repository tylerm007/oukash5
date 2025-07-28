import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './FormulaComponent-card.component.html',
  styleUrls: ['./FormulaComponent-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.FormulaComponent-card]': 'true'
  }
})

export class FormulaComponentCardComponent {


}