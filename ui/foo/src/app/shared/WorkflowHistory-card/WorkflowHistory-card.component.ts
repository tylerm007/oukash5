import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WorkflowHistory-card.component.html',
  styleUrls: ['./WorkflowHistory-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WorkflowHistory-card]': 'true'
  }
})

export class WorkflowHistoryCardComponent {


}