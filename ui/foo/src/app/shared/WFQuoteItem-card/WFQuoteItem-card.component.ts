import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFQuoteItem-card.component.html',
  styleUrls: ['./WFQuoteItem-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFQuoteItem-card]': 'true'
  }
})

export class WFQuoteItemCardComponent {


}