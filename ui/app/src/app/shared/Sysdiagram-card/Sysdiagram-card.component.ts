import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './Sysdiagram-card.component.html',
  styleUrls: ['./Sysdiagram-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.Sysdiagram-card]': 'true'
  }
})

export class SysdiagramCardComponent {


}