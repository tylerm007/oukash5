import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './PrivateLabelTemplate-card.component.html',
  styleUrls: ['./PrivateLabelTemplate-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.PrivateLabelTemplate-card]': 'true'
  }
})

export class PrivateLabelTemplateCardComponent {


}