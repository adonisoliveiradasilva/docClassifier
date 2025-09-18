import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoadingService } from './core/services/loading.service';
import { TopBarComponent } from './shared/molecules/top-bar/top-bar.component';
import { HeaderComponent } from './shared/molecules/header/header.component';
import { CardComponent } from './shared/molecules/card/card.component';
import { ToastContainerComponent } from './shared/molecules/toast-container/toast-container.component';
import { LoadingComponent } from './shared/atoms/loading/loading.component';
import { FeedbackComponent } from './shared/atoms/feedback/feedback.component';
import { FeedbackService } from './core/services/feedback.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    TopBarComponent,
    HeaderComponent,
    CardComponent,
    ToastContainerComponent,
    LoadingComponent,
    FeedbackComponent
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  loadingState$ = this.loadingService.loadingState$;
  feedbackState$ = this.feedbackService.feedbackState$;

  constructor(private loadingService: LoadingService, 
    private feedbackService: FeedbackService
  ) {}
}
