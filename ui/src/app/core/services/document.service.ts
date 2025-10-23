import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, Observable, tap, throwError } from 'rxjs';

export interface AccuracyResponse {
  status_code: number;
  message: string;
  data: {
    predicted_class: string;
    confidence: number;
    all_confidences: { [key: string]: number }; 
  } | null;
}


@Injectable({
  providedIn: 'root'
})
export class DocumentService {
  private readonly apiUrl = 'http://localhost:8000/model/classify_docs';

  http: HttpClient = inject(HttpClient);

  uploadDocument(file: File, docType: string): Observable<AccuracyResponse> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('documentType', docType);

  return this.http.post<AccuracyResponse>(this.apiUrl, formData).pipe(
    tap(res => console.log('Resposta da API:', res)),
    catchError(err => {
      return throwError(() => err);
    })
  );
}
}
