import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFActivityStatus-card.component.html',
  styleUrls: ['./WFActivityStatus-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFActivityStatus-card]': 'true'
  }
})

export class WFActivityStatusCardComponent {


}