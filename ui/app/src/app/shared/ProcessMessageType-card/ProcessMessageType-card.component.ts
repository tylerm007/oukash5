import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './ProcessMessageType-card.component.html',
  styleUrls: ['./ProcessMessageType-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.ProcessMessageType-card]': 'true'
  }
})

export class ProcessMessageTypeCardComponent {


}