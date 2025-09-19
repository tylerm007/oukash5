import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './LaneDefinition-card.component.html',
  styleUrls: ['./LaneDefinition-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.LaneDefinition-card]': 'true'
  }
})

export class LaneDefinitionCardComponent {


}