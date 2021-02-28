import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {Order} from '../models/order';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class OrdersService {
  // url = 'http://localhost:8000/';

  url = 'https://' + window.location.host;

  constructor(private http: HttpClient) {
  }

  getOrders(): Observable<Order[]> {
    return this.http.get<Order[]>(this.url + '/api/order');
  }

  getRoutes(n: number): Observable<any> {
    return this.http.get(this.url + '/admin/' + n);
  }

  pushOrder(order: Order): void {
    const body = {
      order
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
