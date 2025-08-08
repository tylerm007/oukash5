import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './CODETB-card.component.html',
  styleUrls: ['./CODETB-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.CODETB-card]': 'true'
  }
})

export class CODETBCardComponent {


}