import { Injectable } from '@angular/core';
import {
  ToleranceFilter,
  AnomalyFilterRequest,
} from '../models/interfaces/anomaly-filter';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class AnomalyFilterService {
  saveVariablesUrl: string = environment.saveVariablesUrl;
  getVariablesUrl: string = environment.getVariablesUrl;

  constructor(private httpClient: HttpClient) {}

  public getAnomalyFilter(mapId: number): Observable<any> {
    return this.httpClient.get<any>(`${this.saveVariablesUrl}` + mapId);
  }
  public findAnomalyFilterBySectorAndTolerance(
    sectorId: number,
    tolerance: string
  ): Observable<any> {
    return this.httpClient.get<any>(
      `${this.saveVariablesUrl}` +
        sectorId +
        '/' +
        'find_anomaly_filter_by_sector_id_and_tolerance/',
      { params: { tolerance: tolerance } }
    );
  }
  // find_indicator_threshold_by_anomaly_filter
  public getIndicatorThresholdBySectorIdAndTolerance(
    sectorId: number,
    tolerance: string
  ): Observable<any> {
    return this.httpClient.get<any>(
      `${this.getVariablesUrl}` +
        sectorId +
        '/' +
        'find_indicator_threshold_by_sector_id_and_tolerance/',
      { params: { tolerance: tolerance } }
    );
  }

  public saveVariables(
    anomalyFilterRequest: AnomalyFilterRequest
  ): Observable<any> {
    console.log('LLEque', anomalyFilterRequest);
    console.log('this.saveVariablesUrl', this.saveVariablesUrl);
    return this.httpClient.post<any>(
      `${this.saveVariablesUrl}`,
      anomalyFilterRequest
    );
  }
  private _tolerances: ToleranceFilter[] = [
    ToleranceFilter.high,
    ToleranceFilter.low,
    ToleranceFilter.medium,
  ];

  private _indicator_number: number[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  private _number_of_days: number[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

  get tolerances(): ToleranceFilter[] {
    return [...this._tolerances];
  }
  get indicator_number(): number[] {
    return [...this._indicator_number];
  }
  get number_of_days(): number[] {
    return [...this._number_of_days];
  }
}
