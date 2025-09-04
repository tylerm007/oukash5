import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './TaskFlow-card.component.html',
  styleUrls: ['./TaskFlow-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.TaskFlow-card]': 'true'
  }
})

export class TaskFlowCardComponent {


}