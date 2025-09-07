import { Component, EventEmitter, Input, Output } from '@angular/core';
import { IOptionsDocument } from '../../data/models/IOptionsDocument.model';
import { NgFor } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subject } from 'rxjs';

@Component({
  selector: 'app-radio-group',
  standalone: true,
  imports: [NgFor,
    FormsModule 
  ],
  templateUrl: './radio-group.component.html',
  styleUrl: './radio-group.component.scss'
})
export class RadioGroupComponent {
  @Input() options!: IOptionsDocument[];
  @Output() selectedOptionChange = new EventEmitter<IOptionsDocument>();

  selectedOption: string = '';

  onOptionChange(option: IOptionsDocument) {
    this.selectedOptionChange.emit(option); 
  }

}
