import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFUserAdmin-card.component.html',
  styleUrls: ['./WFUserAdmin-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFUserAdmin-card]': 'true'
  }
})

export class WFUserAdminCardComponent {


}