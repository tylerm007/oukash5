import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './FormulaSubmissionComponent-card.component.html',
  styleUrls: ['./FormulaSubmissionComponent-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.FormulaSubmissionComponent-card]': 'true'
  }
})

export class FormulaSubmissionComponentCardComponent {


}