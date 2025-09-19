import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './ProcessStatus-card.component.html',
  styleUrls: ['./ProcessStatus-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.ProcessStatus-card]': 'true'
  }
})

export class ProcessStatusCardComponent {


}