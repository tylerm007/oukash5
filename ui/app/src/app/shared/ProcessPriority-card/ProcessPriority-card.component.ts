import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './ProcessPriority-card.component.html',
  styleUrls: ['./ProcessPriority-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.ProcessPriority-card]': 'true'
  }
})

export class ProcessPriorityCardComponent {


}