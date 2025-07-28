import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './COMPANYCERTDETAIL-card.component.html',
  styleUrls: ['./COMPANYCERTDETAIL-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.COMPANYCERTDETAIL-card]': 'true'
  }
})

export class COMPANYCERTDETAILCardComponent {


}