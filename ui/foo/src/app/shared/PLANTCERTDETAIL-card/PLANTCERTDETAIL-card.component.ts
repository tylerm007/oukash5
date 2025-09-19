import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './PLANTCERTDETAIL-card.component.html',
  styleUrls: ['./PLANTCERTDETAIL-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.PLANTCERTDETAIL-card]': 'true'
  }
})

export class PLANTCERTDETAILCardComponent {


}