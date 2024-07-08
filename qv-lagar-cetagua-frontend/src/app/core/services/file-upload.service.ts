import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FileUploadService {
  private fileLoadedSource = new BehaviorSubject<boolean>(false);
  fileLoaded$ = this.fileLoadedSource.asObservable();

  setFileLoaded(loaded: boolean) {
    this.fileLoadedSource.next(loaded);
  }

  constructor(private httpClient: HttpClient) {
    
   }

}
