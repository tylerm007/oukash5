import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './TaskCommentType-card.component.html',
  styleUrls: ['./TaskCommentType-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.TaskCommentType-card]': 'true'
  }
})

export class TaskCommentTypeCardComponent {


}