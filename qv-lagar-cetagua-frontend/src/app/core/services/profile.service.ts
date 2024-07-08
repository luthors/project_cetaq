import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {
  updateUrl: string = environment.updateProfileUrl;

  constructor(private httpClient: HttpClient,) { }

  updateProfile(name: string, lastName: string, email: string, id:number) {
    return this.httpClient.put(`${this.updateUrl}` + 'user/'+ `${id}` + '/', { name, lastName, email });
  }

  updatePassword(password:string, password2: string, id:number){
    const headers = new HttpHeaders({
      Authorization: 'Bearer ' + localStorage.getItem('authToken'),
    });
    return this.httpClient.post(`${this.updateUrl}` + `${id}` + '/set_password/', { password, password2 }, {headers});

  }
}
