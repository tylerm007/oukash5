import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './RoleAssigment-card.component.html',
  styleUrls: ['./RoleAssigment-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.RoleAssigment-card]': 'true'
  }
})

export class RoleAssigmentCardComponent {


}