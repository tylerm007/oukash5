import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFUserRole-card.component.html',
  styleUrls: ['./WFUserRole-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFUserRole-card]': 'true'
  }
})

export class WFUserRoleCardComponent {


}