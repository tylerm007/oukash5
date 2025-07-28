import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './ProducedIn1Tb-card.component.html',
  styleUrls: ['./ProducedIn1Tb-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.ProducedIn1Tb-card]': 'true'
  }
})

export class ProducedIn1TbCardComponent {


}