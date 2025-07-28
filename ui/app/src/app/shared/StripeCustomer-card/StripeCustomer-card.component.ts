import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './StripeCustomer-card.component.html',
  styleUrls: ['./StripeCustomer-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.StripeCustomer-card]': 'true'
  }
})

export class StripeCustomerCardComponent {


}