import {Component, OnInit} from '@angular/core';
import {OrdersService} from '../services/orders.service';
import {Order} from '../models/order';
import {MockAddOrdersService} from '../services/mock-add-orders.service';

declare var ol: any;

@Component({
  selector: 'app-body-container',
  templateUrl: './body-container.component.html',
  styleUrls: ['./body-container.component.scss']
})
export class BodyContainerComponent implements OnInit {
  latitude: number = 9.1829321;
  longitude: number = 48.7758459;

  vehicleCount = 2;
  customRide: any = {
    location: [],
    destiny: [],
    options: {
      ecological: 0.5,
      time: 0.5,
      comfort: 0.5
    },
  };

  vectorLayer_name = 'vectorLayer_name';

  map: any;

  constructor(private ordersService: OrdersService, public mockService: MockAddOrdersService) {
  }

  ngOnInit(): void {
    this.map = new ol.Map({
      target: 'map',
      layers: [
        new ol.layer.Tile({
          source: new ol.source.OSM()
        })
      ],
      view: new ol.View({
        center: ol.proj.fromLonLat([this.latitude, this.longitude]),
        zoom: 14
      })
    });
    this.ordersService.getOrders().subscribe(
      orders => this.drawOrders(orders, 'red')
    );
  }

  drawOrders(orders: Order[], color: string): any {
    const features: any[] = [];
    orders.forEach(
      order => features.push(
        new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.fromLonLat([
              order.location[0], order.location[1]
            ]))
          }
        )));

    const vectorSource = new ol.source.Vector({
      features
    });
    const vectorLayer = new ol.layer.Vector({
      source: vectorSource,
      style: new ol.style.Style({
        image: new ol.style.Circle({
          radius: 4,
          fill: new ol.style.Fill({color})
        })
      }),
    });

    this.map.addLayer(vectorLayer);

    console.log(this.map.getLayers());
  }

  drawCentroid(centroid: any, color: string): any {
    const features: any[] = [];

    features.push(
      new ol.Feature({
          geometry: new ol.geom.Point(ol.proj.fromLonLat([
            centroid[0], centroid[1]
          ]))
        }
      ));

    const vectorSource = new ol.source.Vector({
      features
    });
    const vectorLayer = new ol.layer.Vector({
      source: vectorSource,
      style: new ol.style.Style({
        image: new ol.style.Circle({
          radius: 10,
          fill: new ol.style.Fill({color})
        })
      }),
    });

    this.map.addLayer(vectorLayer);

    console.log(this.map.getLayers());
  }

  getRoutes(): void {
    const colors = [
      'red', 'purple', 'pink', 'green', 'yellow'
    ];

    this.ordersService.getRoutes(this.vehicleCount).subscribe(
      x => {
        for (let i = 0; i < x.length; i++) {
          this.drawOrders(x[i].order, colors[i]);
          this.drawCentroid(x[i].centroid, colors[i]); //        color: 'rgba(255, 255, 255, 0.5)'

        }
      }
    );
  }


}
