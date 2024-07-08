import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class CustomerInformationService {
  urlCustomer: string = environment.urlCustomer
  downloadMatch : string = environment.downloadMatch
  
  constructor(private httpClient: HttpClient) { }

  uploadFiles(clientsFile: File, sectorFile: File, connectionsFiles: File){
    const headers = new HttpHeaders({
      'Authorization': 'Bearer ' + localStorage.getItem('authToken'),
    });

    const formData = new FormData();
    const blobClientsFile = new Blob([clientsFile], { type: clientsFile.type });
    const blobSectorFile = new Blob([sectorFile], { type: sectorFile.type });
    const blobConnectionsFiles = new Blob([connectionsFiles], { type: connectionsFiles.type });

    formData.append('Acometidas-File', blobConnectionsFiles, connectionsFiles.name);
    formData.append('Sectores-File', blobSectorFile, sectorFile.name);
    formData.append('Contratos-File', blobClientsFile, clientsFile.name);
    
    return this.httpClient.post(`${this.urlCustomer}`, formData,{ headers})

  }

  downloadFile(): Observable<Blob> {
    return this.httpClient.get(`${this.downloadMatch}`, { responseType: 'blob' });
  }
}
