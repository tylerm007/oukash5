import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './TaskRole-card.component.html',
  styleUrls: ['./TaskRole-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.TaskRole-card]': 'true'
  }
})

export class TaskRoleCardComponent {


}