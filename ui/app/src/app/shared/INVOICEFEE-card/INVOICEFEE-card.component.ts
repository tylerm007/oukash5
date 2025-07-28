import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './INVOICEFEE-card.component.html',
  styleUrls: ['./INVOICEFEE-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.INVOICEFEE-card]': 'true'
  }
})

export class INVOICEFEECardComponent {


}