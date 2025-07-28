import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './PLANTTB-card.component.html',
  styleUrls: ['./PLANTTB-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.PLANTTB-card]': 'true'
  }
})

export class PLANTTBCardComponent {


}