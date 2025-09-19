import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFContact-card.component.html',
  styleUrls: ['./WFContact-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFContact-card]': 'true'
  }
})

export class WFContactCardComponent {


}