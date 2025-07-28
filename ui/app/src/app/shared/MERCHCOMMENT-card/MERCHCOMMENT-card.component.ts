import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './MERCHCOMMENT-card.component.html',
  styleUrls: ['./MERCHCOMMENT-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.MERCHCOMMENT-card]': 'true'
  }
})

export class MERCHCOMMENTCardComponent {


}