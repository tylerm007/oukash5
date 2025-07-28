import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './RCTB-card.component.html',
  styleUrls: ['./RCTB-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.RCTB-card]': 'true'
  }
})

export class RCTBCardComponent {


}