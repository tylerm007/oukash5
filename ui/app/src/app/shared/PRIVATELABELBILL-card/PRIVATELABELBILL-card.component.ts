import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './PRIVATELABELBILL-card.component.html',
  styleUrls: ['./PRIVATELABELBILL-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.PRIVATELABELBILL-card]': 'true'
  }
})

export class PRIVATELABELBILLCardComponent {


}