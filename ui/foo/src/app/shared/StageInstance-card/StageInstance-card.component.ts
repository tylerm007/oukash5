import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './StageInstance-card.component.html',
  styleUrls: ['./StageInstance-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.StageInstance-card]': 'true'
  }
})

export class StageInstanceCardComponent {


}