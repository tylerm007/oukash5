import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './TaskType-card.component.html',
  styleUrls: ['./TaskType-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.TaskType-card]': 'true'
  }
})

export class TaskTypeCardComponent {


}