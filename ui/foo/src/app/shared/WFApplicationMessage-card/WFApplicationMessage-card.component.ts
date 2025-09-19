import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFApplicationMessage-card.component.html',
  styleUrls: ['./WFApplicationMessage-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFApplicationMessage-card]': 'true'
  }
})

export class WFApplicationMessageCardComponent {


}