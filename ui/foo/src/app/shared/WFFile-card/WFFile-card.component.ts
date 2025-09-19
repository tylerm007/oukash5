import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFFile-card.component.html',
  styleUrls: ['./WFFile-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFFile-card]': 'true'
  }
})

export class WFFileCardComponent {


}