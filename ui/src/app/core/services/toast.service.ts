import { Injectable } from '@angular/core';
import { Observable, Subject, timer } from 'rxjs';
import { scan, shareReplay, startWith } from 'rxjs/operators';
import { IToast, IToastType } from '../../shared/data/models/IToast.model';

type ToastAction =
  | { type: 'add'; toast: IToast }
  | { type: 'remove'; id: string }
  | { type: 'clear' };

@Injectable({ providedIn: 'root' })
export class ToastService {
  private actions$ = new Subject<ToastAction>();

  // estado: lista de toasts
  readonly toasts$: Observable<IToast[]> = this.actions$.pipe(
    scan((state, action) => {
      switch (action.type) {
        case 'add':    return [...state, action.toast];
        case 'remove': return state.filter(t => t.id !== action.id);
        case 'clear':  return [];
        default:       return state;
      }
    }, [] as IToast[]),
    startWith([]),
    shareReplay({ bufferSize: 1, refCount: true })
  );

  private nextId() { return crypto.randomUUID?.() ?? Math.random().toString(36).slice(2); }

  show(message: string, opts?: Partial<Omit<IToast,'id'|'message'>> & { type?: IToastType }): string {
    const id = this.nextId();
    const toast: IToast = {
      id,
      message,
      type: opts?.type ?? 'info',
      title: opts?.title,
      duration: opts?.duration ?? 4000,
      dismissible: opts?.dismissible ?? true
    };
    console.log('Adicionando toast:', toast); // <- teste
    this.actions$.next({ type: 'add', toast });

    if (toast.duration && toast.duration > 0) {
      timer(toast.duration).subscribe(() => this.remove(id));
    }
    return id;
  }


  success(msg: string, opts?: Omit<Parameters<ToastService['show']>[1], 'type'>) { return this.show(msg, { ...opts, type: 'success' }); }
  error(msg: string,   opts?: Omit<Parameters<ToastService['show']>[1], 'type'>) { return this.show(msg, { ...opts, type: 'error'   }); }
  info(msg: string,    opts?: Omit<Parameters<ToastService['show']>[1], 'type'>) { return this.show(msg, { ...opts, type: 'info'    }); }
  warning(msg: string, opts?: Omit<Parameters<ToastService['show']>[1], 'type'>) { return this.show(msg, { ...opts, type: 'warning' }); }

  remove(id: string) { this.actions$.next({ type: 'remove', id }); }
  clear()            { this.actions$.next({ type: 'clear' }); }
}
