import { Component } from '@angular/core';
import { LogoComponent } from '../../atoms/logo/logo.component';

@Component({
  selector: 'app-top-bar',
  standalone: true,
  imports: [LogoComponent],
  templateUrl: './top-bar.component.html',
  styleUrl: './top-bar.component.scss'
})
export class TopBarComponent {

}
