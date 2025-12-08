import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './StageDefinition-card.component.html',
  styleUrls: ['./StageDefinition-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.StageDefinition-card]': 'true'
  }
})

export class StageDefinitionCardComponent {


}