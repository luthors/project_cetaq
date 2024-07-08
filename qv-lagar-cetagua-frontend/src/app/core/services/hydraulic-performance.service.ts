import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, map, of } from 'rxjs';
import { Observable } from 'rxjs/internal/Observable';
import { HydraulicPerformanceResponse } from '../models/interfaces/hydraulic-performance-response';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class HydraulicPerformanceService {
  performanceHistoryUrl: string = environment.performanceHistoryUrl;
  urlHydraulicPerformance: string = environment.urlHydraulicPerformance;
  constructor(private httpClient: HttpClient) {}

  sendData(
    files: File[],
    city: string,
    sector: string,
    year: number,
    bimester: number
  ): Observable<any> {
    let formData = new FormData();
    const blob = new Blob([files[0]], { type: files[0].type });
    const blob2 = new Blob([files[1]], { type: files[1].type });

    formData.append('Supplied', blob, files[0].name);
    formData.append('Registered', blob2, files[1].name);
    if (files[2]) {
      const blob3 = new Blob([files[2]], { type: files[2].type });
      formData.append('Telelectura', blob3, files[2].name);
    }

    const headers = new HttpHeaders({
      City: city,
      Sector: sector,
      Year: year,
      Bimester: bimester,
    });

    return this.httpClient.post(`${this.urlHydraulicPerformance}`, formData, {
      headers,
    });
  }

  findHydraulicPerformanceBySectorIdAndYearAndBimester(
    sector: number,
    year: number,
    bimester: number
  ) {
    const anomalyRequest: any = {
      'sector': sector,
      'year': year,
      'bimester': bimester,
    };
    return this.httpClient
      .get<any>(
        `${this.performanceHistoryUrl}` +
          'find_hydraulic_performance_by_sector_id_and_year_and_bimester/',
        { params: anomalyRequest }
      )
      .pipe(catchError(error => of([])));
  }

  addHydraulicPerformanceBySector(
    hydraulicPerformance: HydraulicPerformanceResponse
  ): Observable<any> {
    return this.httpClient.post<HydraulicPerformanceResponse>(
      `${this.performanceHistoryUrl}` + 'create_hydraulic_performance/',
      hydraulicPerformance
    );
  }
  findHydraulicPerformanceBySector(sector: number): Observable<any> {
    if (!sector) {
      throw new Error('sector is required');
    }
    if (sector <= 0) {
      throw new Error('sector must be greater than 0');
    }

    return this.httpClient
      .get<HydraulicPerformanceResponse>(
        `${this.performanceHistoryUrl}` +
          sector +
          '/find_hydraulic_performance_by_sector_id/'
      )
      .pipe(catchError(error => of([])));
  }
  deleteHydraulicPerformanceById(id: number): Observable<boolean> {
    return this.httpClient
      .delete(
        `${this.performanceHistoryUrl}` +
          id +
          '/delete_hydraulic_performance_by_id/'
      )
      .pipe(
        map(resp => true),
        catchError(err => of(false))
      );
  }
}
