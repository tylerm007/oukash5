import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './CompanyApplication-card.component.html',
  styleUrls: ['./CompanyApplication-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.CompanyApplication-card]': 'true'
  }
})

export class CompanyApplicationCardComponent {


}