import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ToastService } from '../../../core/services/toast.service';
import { Observable } from 'rxjs';
import { IToast } from '../../data/models/IToast.model'
import { ToastComponent } from '../../atoms/toast/toast.component';

@Component({
  selector: 'app-toast-container',
  standalone: true,
  imports: [CommonModule, ToastComponent],
  templateUrl: './toast-container.component.html',
  styleUrls: ['./toast-container.component.scss']
})
export class ToastContainerComponent {
  toasts$: Observable<IToast[]> = this.toastService.toasts$;

  constructor(private toastService: ToastService) {}
}
