import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFActivityLog-card.component.html',
  styleUrls: ['./WFActivityLog-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFActivityLog-card]': 'true'
  }
})

export class WFActivityLogCardComponent {


}