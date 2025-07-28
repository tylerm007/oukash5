import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './VISIT-card.component.html',
  styleUrls: ['./VISIT-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.VISIT-card]': 'true'
  }
})

export class VISITCardComponent {


}