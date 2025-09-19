import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFRole-card.component.html',
  styleUrls: ['./WFRole-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFRole-card]': 'true'
  }
})

export class WFRoleCardComponent {


}