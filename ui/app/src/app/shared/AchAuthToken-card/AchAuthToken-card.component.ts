import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './AchAuthToken-card.component.html',
  styleUrls: ['./AchAuthToken-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.AchAuthToken-card]': 'true'
  }
})

export class AchAuthTokenCardComponent {


}