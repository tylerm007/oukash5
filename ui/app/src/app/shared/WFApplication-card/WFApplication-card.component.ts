import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFApplication-card.component.html',
  styleUrls: ['./WFApplication-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFApplication-card]': 'true'
  }
})

export class WFApplicationCardComponent {


}