import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './LabelTb-card.component.html',
  styleUrls: ['./LabelTb-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.LabelTb-card]': 'true'
  }
})

export class LabelTbCardComponent {


}