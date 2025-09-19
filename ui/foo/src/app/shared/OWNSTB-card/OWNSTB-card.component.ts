import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './OWNSTB-card.component.html',
  styleUrls: ['./OWNSTB-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.OWNSTB-card]': 'true'
  }
})

export class OWNSTBCardComponent {


}