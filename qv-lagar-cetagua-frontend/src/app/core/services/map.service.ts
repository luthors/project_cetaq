import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})

export class MapService {
  geoJsonUrl: string = environment.listMapUrl ;
  exploitationUrl: string = environment.exploitationUrl ;

  constructor(private httpClient: HttpClient) {}

  //Geojson of the specific map
  public getGeoJson(idMap: number): Observable<any> {
    return this.httpClient
      .get(`${this.geoJsonUrl}` + `${idMap}` + '/')
      .pipe(map((response: any) => response.geojson));
  }

  public getDetailMap(idMap: number): Observable<any> {
    return this.httpClient.get(`${this.geoJsonUrl}` + `${idMap}` + '/');
  }

  //List of the all maps
  public getListMap(): Observable<any> {
    return this.httpClient.get(`${this.geoJsonUrl}`);
  }

  //List of the exploitations
  public getExploitations(): Observable<any> {
    return this.httpClient.get(`${this.exploitationUrl}`);
  }

  //Detail of one exploitation
  public getMap(idExplotaition: number): Observable<any> {
    return this.httpClient.get(
      `${this.exploitationUrl}` + `${idExplotaition}` + '/'
    );
  }
}
