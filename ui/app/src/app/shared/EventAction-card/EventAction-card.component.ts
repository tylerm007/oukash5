import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './EventAction-card.component.html',
  styleUrls: ['./EventAction-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.EventAction-card]': 'true'
  }
})

export class EventActionCardComponent {


}