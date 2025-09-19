import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './TaskDefinition-card.component.html',
  styleUrls: ['./TaskDefinition-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.TaskDefinition-card]': 'true'
  }
})

export class TaskDefinitionCardComponent {


}