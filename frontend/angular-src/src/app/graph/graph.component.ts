import {Component, Input, OnInit} from '@angular/core';
import {ResultService} from "../services/result.service";
import {Observable} from "rxjs/internal/Observable";

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit {

  @Input()
  private type : string;

  @Input()
  private start : string;

  @Input()
  private end : string;

  @Input()
  private capitalBase : number;

  @Input()
  private numberOfShares : number;

  private done : boolean;
  private xaxis : string[];
  private dataset1: any[];
  private dataset2: any[];
  private options: Object;
  private colors: any[];



  constructor(private result : ResultService) {
    this.done = false;
    this.xaxis = [];
    this.dataset1 = [];
    this.dataset2 = [];

    this.options = {
      responsive: true,
      elements: {
        point: {
          radius: 0,
          hitRadius: 10,
          hoverRadius: 5,
        }
      }
    };

    this.colors = [
      {
        backgroundColor: 'rgba(46, 134, 193,0.2)',
        borderColor: 'rgba(46, 134, 193,1)',
        pointBackgroundColor: 'rgba(46, 134, 193,1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(46, 134, 193,0.8)'
      },
      {
        backgroundColor: 'rgba(237, 41, 57,0.2)',
        borderColor: 'rgba(237, 41, 57,1)',
        pointBackgroundColor: 'rgba(237, 41, 57,1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(237, 41, 57,0.8)'
      }];
  }

  ngOnInit() {

    if (this.type === 'apple') {
      console.log(this.start);
      this.extractDataFromAPI(
        this.result.buyAppleResult(this.start, this.end, this.numberOfShares, this.capitalBase)
      );
    }
  }

  public static dateNumToString(num, date: Date) {

    date.setTime(num);

    return date.toDateString().substring(4);
  }

  private extractDataFromAPI(observable : Observable<any>) {
    observable.subscribe(response => {
      let algoToBench = response.algo_to_benchmark;
      let rollingBeta = response.rolling_beta;

      let date = new Date();

      let algo = [];
      let bench = [];

      console.log(algoToBench.data);

      for (let point of algoToBench.data.data01) {
        this.xaxis.push(GraphComponent.dateNumToString(point[0], date));
        algo.push(point[1] * 100);
        bench.push(point[2] * 100);
      }

      this.dataset1.push({
        data: algo,
        label: "Algorithm Return %",
        fill: true,
      });
      this.dataset1.push({
        data: bench,
        label: "Benchmark Return %",
        fill: false,
      });

      let beta = [];

      for (let point of rollingBeta.data.data01) {
        beta.push(point[1] * 100);
      }

      this.dataset2.push({
        data: beta,
        label: "Beta"
      });

      this.done = true;
    });
  }

}
