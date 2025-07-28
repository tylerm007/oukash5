import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './COMPANYSTATUSTB-card.component.html',
  styleUrls: ['./COMPANYSTATUSTB-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.COMPANYSTATUSTB-card]': 'true'
  }
})

export class COMPANYSTATUSTBCardComponent {


}