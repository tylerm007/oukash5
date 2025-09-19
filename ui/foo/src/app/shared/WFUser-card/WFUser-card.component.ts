import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFUser-card.component.html',
  styleUrls: ['./WFUser-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFUser-card]': 'true'
  }
})

export class WFUserCardComponent {


}