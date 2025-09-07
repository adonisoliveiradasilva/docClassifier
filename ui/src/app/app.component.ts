import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TopBarComponent } from './shared/molecules/top-bar/top-bar.component';
import { HeaderComponent } from './shared/molecules/header/header.component';
import { CardComponent } from './shared/molecules/card/card.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, 
    TopBarComponent,
    HeaderComponent,
    CardComponent  
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'ui';
}
