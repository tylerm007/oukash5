import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './COMPANYHOLDTB-card.component.html',
  styleUrls: ['./COMPANYHOLDTB-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.COMPANYHOLDTB-card]': 'true'
  }
})

export class COMPANYHOLDTBCardComponent {


}