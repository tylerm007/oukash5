import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './ProcessMessage-card.component.html',
  styleUrls: ['./ProcessMessage-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.ProcessMessage-card]': 'true'
  }
})

export class ProcessMessageCardComponent {


}