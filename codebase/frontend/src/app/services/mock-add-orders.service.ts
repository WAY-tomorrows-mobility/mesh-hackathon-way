import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {Order} from '../models/order';

@Injectable({
  providedIn: 'root'
})


export class MockAddOrdersService {
  // url = 'http://localhost:8000';
  url = 'https://' + window.location.host;

  start = [9.1829321, 48.7758459];
  maxstep = 0.01;

  n = 10;

  orders: any = [];

  constructor(private http: HttpClient) {

  }

  pushOrders(): void {
    const body = {
      order: {
        location: [
          this.start[0] + Math.random() * this.maxstep,
          this.start[1] + Math.random() * this.maxstep,
        ],
        destiny: this.start,
        options: {
          ecological: Math.random(),
          time: Math.random(),
          comfort: Math.random()
        }
      }
    };

    console.log('Posting ');
    const headers = {'content-type': 'application/json'};
    this.http.post(this.url + '/api/order', body, {headers}).subscribe(
      x => {
        console.log('posted, ', x);
        window.location.reload();
      }
    );
  }
}
