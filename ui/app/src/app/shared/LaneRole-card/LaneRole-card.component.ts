import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './LaneRole-card.component.html',
  styleUrls: ['./LaneRole-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.LaneRole-card]': 'true'
  }
})

export class LaneRoleCardComponent {


}