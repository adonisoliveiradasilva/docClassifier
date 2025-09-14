import { Injectable } from '@angular/core';
import { BehaviorSubject, from, Observable, finalize } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoadingService {
  private _loadingState$ = new BehaviorSubject<boolean>(false);
  loadingState$ = this._loadingState$.asObservable();

  show(): void {
    this._loadingState$.next(true);
  }

  hide(): void {
    this._loadingState$.next(false);
  }

  withLoading<T>(source: Observable<T> | Promise<T>): Observable<T> {
    this.show();
    return from(source).pipe(
      finalize(() => this.hide())
    );
  }
}
