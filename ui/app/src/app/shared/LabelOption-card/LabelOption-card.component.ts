import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './LabelOption-card.component.html',
  styleUrls: ['./LabelOption-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.LabelOption-card]': 'true'
  }
})

export class LabelOptionCardComponent {


}