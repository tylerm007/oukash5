import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFQuote-card.component.html',
  styleUrls: ['./WFQuote-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFQuote-card]': 'true'
  }
})

export class WFQuoteCardComponent {


}