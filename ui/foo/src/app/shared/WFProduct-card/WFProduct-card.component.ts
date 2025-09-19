import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFProduct-card.component.html',
  styleUrls: ['./WFProduct-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFProduct-card]': 'true'
  }
})

export class WFProductCardComponent {


}