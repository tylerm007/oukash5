import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './PLANTSTATUSTB-card.component.html',
  styleUrls: ['./PLANTSTATUSTB-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.PLANTSTATUSTB-card]': 'true'
  }
})

export class PLANTSTATUSTBCardComponent {


}