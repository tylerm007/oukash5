import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './MERCHOTHERNAME-card.component.html',
  styleUrls: ['./MERCHOTHERNAME-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.MERCHOTHERNAME-card]': 'true'
  }
})

export class MERCHOTHERNAMECardComponent {


}