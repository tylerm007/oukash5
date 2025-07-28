import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './ProductJob-card.component.html',
  styleUrls: ['./ProductJob-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.ProductJob-card]': 'true'
  }
})

export class ProductJobCardComponent {


}