import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class IndicatorThresholdService {
  listThresholdUrl: string = environment.listThresholdUrl;
  constructor(private httpClient: HttpClient) {}

  public getIndicatorsList(): Observable<any> {
    return this.httpClient.get(`${this.listThresholdUrl}`);
  }

  public getThresholdList(idIndicator: number): Observable<any> {
    return this.httpClient.get(`${this.listThresholdUrl}` + `${idIndicator}`);
  }
}
