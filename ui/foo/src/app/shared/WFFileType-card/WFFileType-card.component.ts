import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFFileType-card.component.html',
  styleUrls: ['./WFFileType-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFFileType-card]': 'true'
  }
})

export class WFFileTypeCardComponent {


}