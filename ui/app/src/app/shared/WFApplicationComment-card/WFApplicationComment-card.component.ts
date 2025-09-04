import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFApplicationComment-card.component.html',
  styleUrls: ['./WFApplicationComment-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFApplicationComment-card]': 'true'
  }
})

export class WFApplicationCommentCardComponent {


}