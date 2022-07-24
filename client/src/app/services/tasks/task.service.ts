import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import {Observable} from 'rxjs';

export interface Task{ 
  id: number,
  title: string,
  subtitle: string,
  deadline: string,
  category: string,
  priority: string,
  workers: Workers[],
}

export interface Workers{ 
  worker_id: number,
  username: string,
  finished: boolean
}


@Injectable({
  providedIn: 'root',
})
export class TaskService {
  private BASE_API_URL = 'http://127.0.0.1:5000/api/tasks';

  private options: any;

  constructor(private client: HttpClient) {
    this.options = {
      headers: {
        'x-access-tokens': localStorage.getItem('jwt'),
      },
    };
  }

  getTasks(): Observable<any> {
    return this.client.get(this.BASE_API_URL, this.options)
  }

  getTaskById(id: any): Observable<any>{ 
    const url = this.BASE_API_URL +"/"+id
    return this.client.get(url, this.options);
  }

  save(task: Task): Observable<any>{ 
    return this.client.post(this.BASE_API_URL, task, this.options);
  }

  update(task: Task): Observable<any>{ 
    const url = this.BASE_API_URL +"/"+task.id
    return this.client.put(url, task, this.options);
  }

  del(id: any): Observable<any> { 
    const url = this.BASE_API_URL +"/"+id
    console.log(url)
    return this.client.delete(url, this.options);
  }

}
