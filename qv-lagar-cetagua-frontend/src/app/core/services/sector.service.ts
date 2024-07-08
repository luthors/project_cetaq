import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, map } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class SectorService {
  listSectorUrl : string = environment.listMapUrl ;
  
  constructor(private httpClient: HttpClient) {}

  public getSector(idMap: number): Observable<any> {
    return this.httpClient.get(
      `${this.listSectorUrl}`+ `${idMap}` + '/find_sector_on_map' 
    );
  }
  
}
