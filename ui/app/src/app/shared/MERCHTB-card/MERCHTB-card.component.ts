import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './MERCHTB-card.component.html',
  styleUrls: ['./MERCHTB-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.MERCHTB-card]': 'true'
  }
})

export class MERCHTBCardComponent {


}