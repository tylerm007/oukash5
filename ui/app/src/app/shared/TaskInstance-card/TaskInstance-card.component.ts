import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './TaskInstance-card.component.html',
  styleUrls: ['./TaskInstance-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.TaskInstance-card]': 'true'
  }
})

export class TaskInstanceCardComponent {


}