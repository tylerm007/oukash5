import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './TaskStatus-card.component.html',
  styleUrls: ['./TaskStatus-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.TaskStatus-card]': 'true'
  }
})

export class TaskStatusCardComponent {


}