import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './ProductJobLineItem-card.component.html',
  styleUrls: ['./ProductJobLineItem-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.ProductJobLineItem-card]': 'true'
  }
})

export class ProductJobLineItemCardComponent {


}