import { Component, OnInit, EventEmitter, Input, Output, Inject } from '@angular/core';
import {
  NgxFileDropEntry,
  FileSystemFileEntry,
  FileSystemDirectoryEntry,
} from 'ngx-file-drop';

import {
  trigger,
  state,
  style,
  animate,
  transition,
} from '@angular/animations';
import {
  HttpClient,
  HttpEventType,
  HttpRequest,
  HttpErrorResponse,
} from '@angular/common/http';
import { catchError, last, map, tap } from 'rxjs';
import { FileUploadModel } from 'src/app/core/models/fileUploadModel';
import { of } from 'rxjs';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { FileUploadService } from 'src/app/core/services/file-upload.service';
import Swal from 'sweetalert2';
import { control } from 'leaflet';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file.upload.component.html',
  styleUrls: ['./file.upload.component.scss'],
  animations: [
    trigger('fadeInOut', [
      state('in', style({ opacity: 100 })),
      transition('* => void', [animate('300ms', style({ opacity: 0 }))]),
    ]),
  ],
})
export class FileUploadComponent {
  public fileLoaded: boolean = false;
  allowedExtensions: string[] = [];
  requiredNames : string[] = [];
  optional: boolean = false

  @Output() filesLoaded: EventEmitter<File> = new EventEmitter();

  constructor(
    public dialogRef: MatDialogRef<FileUploadComponent>,
     @Inject(MAT_DIALOG_DATA) public data: any,
     private fileUploadService: FileUploadService) { }

  public files: NgxFileDropEntry[] = [];

  /**
   * Method that is executed when files are dropped into the designated area
   * @param files Array of NgxFileDropEntry objects representing dropped files
   */
  public dropped(files: NgxFileDropEntry[]) {
    this.files= files

    this.requiredNames = this.data.requiredNames;
    this.optional = this.data.optional

    for (const droppedFile of files) {
      if (droppedFile.fileEntry.isFile) {
        const fileEntry = droppedFile.fileEntry as FileSystemFileEntry;
        fileEntry.file((file: File) => {
          if (!this.typeOfFile(file.name)) {
            Swal.fire('¡Error!', 'Ingrese un fichero con formato válido.<br><br>El fichero debe ser formato' + this.data.allowedExtensions , 'error');
            this.resetFiles();
            return;
          }
          
          this.filesLoaded.emit(file);

          const formData = new FormData();
          formData.append('logo', file, droppedFile.relativePath);

          // Service active and change the value of the fileloaded variable
          this.fileUploadService.setFileLoaded(true);
          this.fileLoaded = true;
        });
      } else {
        // It was a directory (empty directories are added, otherwise only files)
        const fileEntry = droppedFile.fileEntry as FileSystemDirectoryEntry;
        console.log(droppedFile.relativePath, fileEntry);
      }
    }

  }


  public fileOver(event: any) {
    console.log(event);
  }

  public fileLeave(event: any) {
    console.log(event);
  }

  /**
   * Close the modal
   */
  closeModal(): void {
    this.dialogRef.close();
  }

  /**
   * Function with the validate process after press 'acept' on the modal element
   * @returns An error message and resets the file selection if there are no files inside the allowed range or they are invalid
   */
  aceptModal(): void{
    if (!this.numberOfFiles()) {
      Swal.fire('¡Error!', 'Número de archivos no válido', 'error');
      this.resetFiles();
      return;
    }

    if (!this.validateFiles()) {
      this.resetFiles();
      return;
    }

    this.dialogRef.close('success');
    
  }

  /**
   * This function validate file extension
   * @param fileName is the string with the name file to validate
   * @returns Boolean value, if the extension is allow returns true, otherwise it returns false
   */
  typeOfFile(fileName: string): boolean {
    return this.data.allowedExtensions.some((ext: string) => fileName.endsWith(ext));
  }

  /**
   * This fuction validate the number of files
   * @returns Boolean value, if it is inside the range returns true, otherwise it returns false 
   */
  numberOfFiles(): boolean{
    const fileNumbers = this.files.length
    return ((fileNumbers >= this.data.minFiles) && (fileNumbers <= this.data.maxFiles))
  }
  
  /**
   * Reset the file array
   */
  resetFiles() {
    this.files = [];
  }

  /**
   * This function validate de required files names 
   * @returns Boolean value, if there are all the required files returns true, otherwise it return false
   */
  validateFiles(): boolean {
    if (this.data.validateName) {
      let reviewRequiredNames = this.requiredNames
      let matchItems: any[] = []; 
      let vectorPrueba: any[] =[]
      // This iterates over the files to check if they match the required names
      for (let i = 0; i < this.files.length; i++) {
        vectorPrueba.push(this.files[i].fileEntry.name.split('.').slice(0, -1).join('.'))
        const fileName = vectorPrueba[i];

        // Check if the file name matches at least one of the required names
        if (reviewRequiredNames.includes(fileName)) {
          matchItems.push(this.files[i]); // Add the file to matchItems if it matches
          // Remove the file name from reviewRequiredNames
          reviewRequiredNames = reviewRequiredNames.filter(name => name !== fileName);
        }
      }

      // Check if all the required files were found
      if (matchItems.length < this.requiredNames.length) {
        Swal.fire('¡Error!', 'Se requieren los ficheros obligatorios para el cálculo', 'error');
        return false
      }
      if (this.optional && this.files.length > this.requiredNames.length) {
        return true; 
      } else if (this.files.length === this.requiredNames.length) {
        return true;
      } 
      
    }
    return true;
  }
}

