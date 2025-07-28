import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Billing-card.component.html',
  styleUrls: ['./Billing-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Billing-card]': 'true'
  }
})

export class BillingCardComponent {


}