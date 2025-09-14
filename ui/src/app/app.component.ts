import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoadingService } from './core/services/loading.service';
import { TopBarComponent } from './shared/molecules/top-bar/top-bar.component';
import { HeaderComponent } from './shared/molecules/header/header.component';
import { CardComponent } from './shared/molecules/card/card.component';
import { ToastContainerComponent } from './shared/molecules/toast-container/toast-container.component';
import { LoadingComponent } from './shared/atoms/loading/loading.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    TopBarComponent,
    HeaderComponent,
    CardComponent,
    ToastContainerComponent,
    LoadingComponent
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  loadingState$ = this.loadingService.loadingState$;

  constructor(private loadingService: LoadingService) {}
}
