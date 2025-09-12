export type IToastType = 'success' | 'error' | 'info' | 'warning';

export interface IToast {
  id: string;
  type: IToastType;
  message: string;
  title?: string;
  duration?: number;  
  dismissible?: boolean; 
}
