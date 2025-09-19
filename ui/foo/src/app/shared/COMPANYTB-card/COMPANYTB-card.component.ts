import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './COMPANYTB-card.component.html',
  styleUrls: ['./COMPANYTB-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.COMPANYTB-card]': 'true'
  }
})

export class COMPANYTBCardComponent {


}