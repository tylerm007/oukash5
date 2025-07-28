import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './CompanycontactsTb-card.component.html',
  styleUrls: ['./CompanycontactsTb-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.CompanycontactsTb-card]': 'true'
  }
})

export class CompanycontactsTbCardComponent {


}