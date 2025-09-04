import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './TaskComment-card.component.html',
  styleUrls: ['./TaskComment-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.TaskComment-card]': 'true'
  }
})

export class TaskCommentCardComponent {


}