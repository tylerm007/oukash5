import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFUSERADMIN-card.component.html',
  styleUrls: ['./WFUSERADMIN-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFUSERADMIN-card]': 'true'
  }
})

export class WFUSERADMINCardComponent {


}