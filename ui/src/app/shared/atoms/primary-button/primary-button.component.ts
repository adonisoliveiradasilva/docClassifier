import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { BehaviorSubject, from } from 'rxjs';
import { finalize } from 'rxjs/operators';

@Component({
  selector: 'app-primary-button',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './primary-button.component.html',
  styleUrl: './primary-button.component.scss'
})
export class PrimaryButtonComponent {
  @Input() label!: string;
  @Input() action!: () => Promise<unknown>;

  loading$ = new BehaviorSubject<boolean>(false);

  handleClick() {
    if (!this.action || this.loading$.value) return;

    this.loading$.next(true);
    from(this.action())
      .pipe(finalize(() => this.loading$.next(false)))
      .subscribe();
  }

}
