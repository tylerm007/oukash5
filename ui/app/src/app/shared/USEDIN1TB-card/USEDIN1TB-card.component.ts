import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './USEDIN1TB-card.component.html',
  styleUrls: ['./USEDIN1TB-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.USEDIN1TB-card]': 'true'
  }
})

export class USEDIN1TBCardComponent {


}