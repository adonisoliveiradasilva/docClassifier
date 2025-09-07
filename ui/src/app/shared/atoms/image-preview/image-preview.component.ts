import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-image-preview',
  standalone: true,
  imports: [],
  templateUrl: './image-preview.component.html',
  styleUrl: './image-preview.component.scss'
})
export class ImagePreviewComponent {
  @Input() previewUrl: string | null = null;
  
}
