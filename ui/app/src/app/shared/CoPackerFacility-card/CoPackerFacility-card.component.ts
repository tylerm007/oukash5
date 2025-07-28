import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './CoPackerFacility-card.component.html',
  styleUrls: ['./CoPackerFacility-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.CoPackerFacility-card]': 'true'
  }
})

export class CoPackerFacilityCardComponent {


}