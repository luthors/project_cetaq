import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})

export class HelpInformationService {
helpInformationurl: string = environment.helpInformationurl
helpInfovariablesurl: string = environment.helpInfovariablesurl
constructor(private http: HttpClient) { }


getHelpInformation() {
  return this.http.get<any>(`${this.helpInformationurl}`);
}

getHelpInfoVariables() {
  return this.http.get<any>(`${this.helpInfovariablesurl}`);
}
}
