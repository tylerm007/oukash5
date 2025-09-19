import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './FormulaSubmissionPlant-card.component.html',
  styleUrls: ['./FormulaSubmissionPlant-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.FormulaSubmissionPlant-card]': 'true'
  }
})

export class FormulaSubmissionPlantCardComponent {


}