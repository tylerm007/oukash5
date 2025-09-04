import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFCompany-card.component.html',
  styleUrls: ['./WFCompany-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFCompany-card]': 'true'
  }
})

export class WFCompanyCardComponent {


}