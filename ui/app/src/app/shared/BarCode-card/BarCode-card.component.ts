import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './BarCode-card.component.html',
  styleUrls: ['./BarCode-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.BarCode-card]': 'true'
  }
})

export class BarCodeCardComponent {


}