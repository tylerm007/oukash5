import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './INVOICEFEESDETAIL-card.component.html',
  styleUrls: ['./INVOICEFEESDETAIL-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.INVOICEFEESDETAIL-card]': 'true'
  }
})

export class INVOICEFEESDETAILCardComponent {


}