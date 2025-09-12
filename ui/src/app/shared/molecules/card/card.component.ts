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

  constructor(private documentService: DocumentService, private toast: ToastService) {
  }

  ngOnInit() {
    setTimeout(() => this.toast.success('Toast do AppComponent', { title: 'Teste' }), 2000);
  }

  get getOptionsDocument(): IOptionsDocument[] {
    return this._optionsDocument;
  }

  handleSelected(event: IOptionsDocument) {
    this.selectedDocType = event.slug;
    console.log('Opção selecionada:', event);
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
    if (!this.selectedFile || !this.selectedDocType) return;

    try {
      console.log('Chamando a API...');
      const result = await firstValueFrom(
        this.documentService.uploadDocument(this.selectedFile, this.selectedDocType)
      );
      this.accuracyResult = result;
      console.log('Resultado da API:', result);
      this.state$.next(CardState.FEEDBACK);
    } catch (err) {
      console.error('Erro no envio:', err);
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
  }
}
