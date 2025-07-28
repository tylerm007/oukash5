import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './LabelComment-card.component.html',
  styleUrls: ['./LabelComment-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.LabelComment-card]': 'true'
  }
})

export class LabelCommentCardComponent {


}