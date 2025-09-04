import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFApplicationStatus-card.component.html',
  styleUrls: ['./WFApplicationStatus-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFApplicationStatus-card]': 'true'
  }
})

export class WFApplicationStatusCardComponent {


}