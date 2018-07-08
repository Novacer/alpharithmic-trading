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



  constructor(private result : ResultService) {
    this.done = false;
    this.xaxis = [];
    this.dataset1 = [];
    this.dataset2 = [];
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
        label: "Algorithm Return %"
      });
      this.dataset1.push({
        data: bench,
        label: "Benchmark Return %"
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
