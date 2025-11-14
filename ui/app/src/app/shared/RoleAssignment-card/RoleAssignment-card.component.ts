import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './RoleAssignment-card.component.html',
  styleUrls: ['./RoleAssignment-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.RoleAssignment-card]': 'true'
  }
})

export class RoleAssignmentCardComponent {


}