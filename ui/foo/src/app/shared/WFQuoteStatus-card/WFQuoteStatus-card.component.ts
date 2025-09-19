import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFQuoteStatus-card.component.html',
  styleUrls: ['./WFQuoteStatus-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFQuoteStatus-card]': 'true'
  }
})

export class WFQuoteStatusCardComponent {


}