import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './ProcessInstance-card.component.html',
  styleUrls: ['./ProcessInstance-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.ProcessInstance-card]': 'true'
  }
})

export class ProcessInstanceCardComponent {


}