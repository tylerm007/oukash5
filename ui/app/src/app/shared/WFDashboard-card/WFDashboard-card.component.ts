import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './WFDashboard-card.component.html',
  styleUrls: ['./WFDashboard-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.WFDashboard-card]': 'true'
  }
})

export class WFDashboardCardComponent {


}