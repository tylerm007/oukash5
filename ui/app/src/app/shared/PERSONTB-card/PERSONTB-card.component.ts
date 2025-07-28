import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './PERSONTB-card.component.html',
  styleUrls: ['./PERSONTB-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.PERSONTB-card]': 'true'
  }
})

export class PERSONTBCardComponent {


}