import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './ProcessDefinition-card.component.html',
  styleUrls: ['./ProcessDefinition-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.ProcessDefinition-card]': 'true'
  }
})

export class ProcessDefinitionCardComponent {


}