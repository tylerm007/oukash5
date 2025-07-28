import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './CompanyPlantOption-card.component.html',
  styleUrls: ['./CompanyPlantOption-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.CompanyPlantOption-card]': 'true'
  }
})

export class CompanyPlantOptionCardComponent {


}