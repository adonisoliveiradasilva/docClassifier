import { Injectable } from '@angular/core';
import { BehaviorSubject, from, Observable, finalize } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FeedbackService {
  private readonly _feedbackState$ = new BehaviorSubject<string>('');
  feedbackState$ = this._feedbackState$.asObservable();

  activate(message: string): void {
    this._feedbackState$.next(message);
  }

  clear(): void{
    console.log('LIMPANDO')
    this._feedbackState$.next('');
  }

}
