import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, Observable, tap, throwError } from 'rxjs';

export interface AccuracyResponse {
  acuracias: { [key: string]: number }[];
  mensagem: string;
}

@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  private readonly apiUrl = 'http://localhost:8000/api/prediction'; // ajuste conforme sua API

  http: HttpClient = inject(HttpClient);

  uploadDocument(file: File, docType: string): Observable<AccuracyResponse> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('documentType', docType);

  return this.http.post<any>(this.apiUrl, formData).pipe(
    tap(res => console.log('Resposta da API:', res)),
    catchError(err => {
      console.error('Erro na API:', err);
      return throwError(() => err);
    })
  );
}
}
