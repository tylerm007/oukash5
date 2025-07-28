import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './YoshonInfo-card.component.html',
  styleUrls: ['./YoshonInfo-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.YoshonInfo-card]': 'true'
  }
})

export class YoshonInfoCardComponent {


}