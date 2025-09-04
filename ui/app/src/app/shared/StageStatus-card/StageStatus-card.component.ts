import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './StageStatus-card.component.html',
  styleUrls: ['./StageStatus-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.StageStatus-card]': 'true'
  }
})

export class StageStatusCardComponent {


}