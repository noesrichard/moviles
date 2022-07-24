import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Observable} from 'rxjs';

export interface User {
  id?: number;
  username: string;
  password: string;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private BASE_API_URL = 'http://127.0.0.1:5000/api';

  constructor(private client: HttpClient) {}

  signin(user: User): Observable<any>{
    const options = { headers: { 
      "Authorization": "Basic "+btoa(`${user.username}:${user.password}`),
    } };
    const url = this.BASE_API_URL + '/login';
    return this.client.get(url, options)
  }
}
