import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './MiniCRMAction-card.component.html',
  styleUrls: ['./MiniCRMAction-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.MiniCRMAction-card]': 'true'
  }
})

export class MiniCRMActionCardComponent {


}