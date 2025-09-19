import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFIngredient-card.component.html',
  styleUrls: ['./WFIngredient-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFIngredient-card]': 'true'
  }
})

export class WFIngredientCardComponent {


}