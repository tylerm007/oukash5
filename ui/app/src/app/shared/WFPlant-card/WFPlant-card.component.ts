import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFPlant-card.component.html',
  styleUrls: ['./WFPlant-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFPlant-card]': 'true'
  }
})

export class WFPlantCardComponent {


}