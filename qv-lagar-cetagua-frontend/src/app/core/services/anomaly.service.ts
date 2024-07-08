import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AnomalyService {
  urlAnomaly: string = environment.urlAnomaly;

  constructor(private httpClient: HttpClient) {}

  public getAnomalyResponseCetaqua(): Observable<any> {
    //endpoint for cetaqua header
    return this.httpClient.get('assets/json/anomaly-response-cetaqua1.json');
  }

  public getAnomalySector(
    city: string,
    daysAnalize: string,
    numberIndicators: string,
    archivo: File,
    parametros: any
  ) {
    const headers = new HttpHeaders({
      'City': city,
      'Analyze-Days': parseInt(daysAnalize),
      'Indicators-Days': parseInt(numberIndicators),
      'Authorization': 'Bearer ' + localStorage.getItem('authToken'),
    });

    const formData = new FormData();
    const blob = new Blob([archivo], { type: archivo.type });
    formData.append('File', blob, archivo.name);
    formData.append('Parameters', JSON.stringify(parametros));

    return this.httpClient.post(`${this.urlAnomaly}`, formData, { headers });
  }
}
