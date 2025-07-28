import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './PERSONJOBTB-card.component.html',
  styleUrls: ['./PERSONJOBTB-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.PERSONJOBTB-card]': 'true'
  }
})

export class PERSONJOBTBCardComponent {


}