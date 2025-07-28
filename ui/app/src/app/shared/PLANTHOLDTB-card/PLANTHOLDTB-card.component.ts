import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './PLANTHOLDTB-card.component.html',
  styleUrls: ['./PLANTHOLDTB-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.PLANTHOLDTB-card]': 'true'
  }
})

export class PLANTHOLDTBCardComponent {


}