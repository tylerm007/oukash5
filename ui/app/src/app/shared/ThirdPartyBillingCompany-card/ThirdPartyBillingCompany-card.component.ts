import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './ThirdPartyBillingCompany-card.component.html',
  styleUrls: ['./ThirdPartyBillingCompany-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.ThirdPartyBillingCompany-card]': 'true'
  }
})

export class ThirdPartyBillingCompanyCardComponent {


}