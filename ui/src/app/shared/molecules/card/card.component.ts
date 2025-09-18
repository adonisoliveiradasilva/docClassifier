import { Component, ElementRef, ViewChild } from '@angular/core';
import { BehaviorSubject, firstValueFrom } from 'rxjs';
import { PrimaryButtonComponent } from '../../atoms/primary-button/primary-button.component';
import { IOptionsDocument } from '../../data/models/IOptionsDocument.model';
import { RadioGroupComponent } from '../../atoms/radio-group/radio-group.component';
import { optionsDocument } from '../../../data/optionsDocument.data';
import { CardState } from '../../data/enums/card.enum';
import { CommonModule } from '@angular/common';
import { ImagePreviewComponent } from '../../atoms/image-preview/image-preview.component';
import { DocumentService, AccuracyResponse } from '../../../core/services/document.service';
import { ToastService } from '../../../core/services/toast.service';
import { LoadingService } from '../../../core/services/loading.service';
import { FeedbackService } from '../../../core/services/feedback.service';

@Component({
  selector: 'app-card',
  standalone: true,
  imports: [
    CommonModule,
    PrimaryButtonComponent,
    RadioGroupComponent,
    ImagePreviewComponent
  ],
  templateUrl: './card.component.html',
  styleUrl: './card.component.scss'
})
export class CardComponent {
  private _optionsDocument: IOptionsDocument[] = optionsDocument;
  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;

  state$ = new BehaviorSubject<CardState>(CardState.EMPTY);
  selectedFile: File | null = null;
  previewUrl: string | null = null;
  selectedDocType: string | null = null;
  accuracyResult: AccuracyResponse | null = null;

  constructor(private documentService: DocumentService, 
    private toast: ToastService,
    private loadingService: LoadingService,
    private feedbackService: FeedbackService
  ) { }

  get getOptionsDocument(): IOptionsDocument[] {
    return this._optionsDocument;
  }

  handleSelected(event: IOptionsDocument) {
    this.selectedDocType = event.slug;
  }

  onUpload = (): Promise<void> => {
    return new Promise(resolve => {
      this.fileInput.nativeElement.click();
      resolve();
    });
  };

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (!input.files || input.files.length === 0) return;

    const file = input.files[0];
    this.handleUpload(file);
  }

  onRemove = (): Promise<void> => {
    return new Promise(resolve => {
      this.handleRemove();
      resolve();
    });
  };

  onSend = async (): Promise<void> => {
    if (!this.selectedFile || !this.selectedDocType) {
      this.toast.warning('Preencha o tipo de documento!');
      return;
    }

    const allowedTypes = ['image/png', 'image/jpeg'];
    if (!allowedTypes.includes(this.selectedFile.type)) {
      this.toast.error('Formato inválido! Selecione um PNG ou JPEG');
      return;
    }

    try {
      // Requisição com loading automático
      const result = await firstValueFrom(
        this.loadingService.withLoading(
          this.documentService.uploadDocument(this.selectedFile, this.selectedDocType)
        )
      );

      if (result.status === 200) {
        this.toast.success(result.message, { title: 'Sucesso' });
        this.feedbackService.activate(result.message)
        this.state$.next(CardState.FEEDBACK);
      } else {
        this.toast.error(result.message || 'Erro desconhecido');
      }

      this.accuracyResult = result;

    } catch (err) {
      console.error('Erro no envio:', err);
      this.toast.error('Erro ao obter resposta da API!');
    }
  };

  onNewUpload = (): Promise<void> => {
    return new Promise(resolve => {
      this.handleNewUpload();
      resolve();
    });
  };

  private handleUpload(file: File) {
    this.selectedFile = file;
    this.previewUrl = URL.createObjectURL(file);
    this.state$.next(CardState.WITH_IMAGE);
  }

  private handleRemove() {
    this.selectedFile = null;
    this.previewUrl = null;
    this.state$.next(CardState.EMPTY);
  }

  private handleNewUpload() {
    this.selectedFile = null;
    this.previewUrl = null;
    this.accuracyResult = null;
    this.state$.next(CardState.EMPTY);
    this.feedbackService.clear()
  }
}
