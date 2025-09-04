import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFPriority-card.component.html',
  styleUrls: ['./WFPriority-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFPriority-card]': 'true'
  }
})

export class WFPriorityCardComponent {


}