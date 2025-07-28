import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './AchStripePayment-card.component.html',
  styleUrls: ['./AchStripePayment-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.AchStripePayment-card]': 'true'
  }
})

export class AchStripePaymentCardComponent {


}