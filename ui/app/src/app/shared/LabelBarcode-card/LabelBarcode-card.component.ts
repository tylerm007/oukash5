import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './LabelBarcode-card.component.html',
  styleUrls: ['./LabelBarcode-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.LabelBarcode-card]': 'true'
  }
})

export class LabelBarcodeCardComponent {


}