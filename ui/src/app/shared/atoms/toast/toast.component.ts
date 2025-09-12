import { Component, Input } from '@angular/core';
import { IToast, IToastType } from '../../data/models/IToast.model';
import { Observable } from 'rxjs';
import { ToastService } from '../../../core/services/toast.service';

@Component({
  selector: 'app-toast',
  standalone: true,
  imports: [],
  templateUrl: './toast.component.html',
  styleUrl: './toast.component.scss'
})
export class ToastComponent {
  @Input() id!: string;
  @Input() type: IToastType = 'info';
  @Input() message: string = '';


  constructor(private toastService: ToastService) {}

  closeToast(id: string){
    this.toastService.remove(id)
  }
}
