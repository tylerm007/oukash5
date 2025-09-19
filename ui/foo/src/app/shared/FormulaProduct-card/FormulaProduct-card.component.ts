import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './FormulaProduct-card.component.html',
  styleUrls: ['./FormulaProduct-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.FormulaProduct-card]': 'true'
  }
})

export class FormulaProductCardComponent {


}