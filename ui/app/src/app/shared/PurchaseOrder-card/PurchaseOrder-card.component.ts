import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './PurchaseOrder-card.component.html',
  styleUrls: ['./PurchaseOrder-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.PurchaseOrder-card]': 'true'
  }
})

export class PurchaseOrderCardComponent {


}