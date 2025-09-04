import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './TaskCategory-card.component.html',
  styleUrls: ['./TaskCategory-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.TaskCategory-card]': 'true'
  }
})

export class TaskCategoryCardComponent {


}