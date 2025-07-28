import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './AchStripePaymentDetail-card.component.html',
  styleUrls: ['./AchStripePaymentDetail-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.AchStripePaymentDetail-card]': 'true'
  }
})

export class AchStripePaymentDetailCardComponent {


}