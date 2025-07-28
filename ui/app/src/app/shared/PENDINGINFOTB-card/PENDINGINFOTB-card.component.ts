import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './PENDINGINFOTB-card.component.html',
  styleUrls: ['./PENDINGINFOTB-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.PENDINGINFOTB-card]': 'true'
  }
})

export class PENDINGINFOTBCardComponent {


}