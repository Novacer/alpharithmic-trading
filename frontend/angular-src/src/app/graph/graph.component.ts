import {Component, Input, OnDestroy, OnInit} from '@angular/core';
import {ResultService} from "../services/result.service";
import {interval} from "rxjs";
import {ScrollToService} from "@nicky-lenaers/ngx-scroll-to";
import {Subscription} from "rxjs/internal/Subscription";
import {Observable} from "rxjs/internal/Observable";

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit, OnDestroy {

  @Input()
  private type: string;

  @Input()
  private start: string;

  @Input()
  private end: string;

  @Input()
  private capitalBase: number;

  @Input()
  private numberOfShares: number;

  @Input()
  private ticker: string;

  @Input()
  private minutes: number;

  public done: boolean;
  public finalAlpha: number;

  private xaxis: string[];
  private dataset1: any[];
  private dataset2: any[];
  private options: Object;
  private colors: any[];

  private logChannel: string;
  private ws: WebSocket;
  private log: string;

  private jobId: string;
  private subscription: Subscription;

  constructor(private result: ResultService, private scroll: ScrollToService) {
    this.done = false;
    this.logChannel = null;
    this.xaxis = [];
    this.dataset1 = [];
    this.dataset2 = [];
    this.ws = null;
    this.log = "";
    this.jobId = null;
    this.subscription = null;

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

    this.logChannel = GraphComponent.generateRandomString();

    this.ws = new WebSocket("ws://alpharithmic.herokuapp.com/ws/logs/" + this.logChannel + "/");
    this.ws.onmessage = (event) => {
      let msg = JSON.parse(event.data).message;
      this.log = this.log.concat(msg, "\n");
    };

    if (this.type === 'apple') {

      this.result.buyAppleResult(this.start, this.end,
        this.numberOfShares, this.capitalBase, this.logChannel).subscribe(response => {
        if (!response) {
          alert("Something went wrong!");
        }
        else {
          this.jobId = response.job_id;

          this.log = this.log.concat("Request was queued, please be patient as it runs.", "\n");

          this.subscription = interval(3000).subscribe(repeat => {
            this.extractDataFromAPI(this.result.fetchResult(this.jobId));
          });
        }
      });
    }

    else if (this.type === 'mean-rev') {

      this.result.meanReversionResult(this.start, this.end,
        this.numberOfShares, this.capitalBase, this.logChannel).subscribe(response => {
        if (!response) {
          alert("Something went wrong!");
        }
        else {
          this.jobId = response.job_id;

          this.log = this.log.concat("Request was queued, please be patient as it runs.", "\n");

          this.subscription = interval(3000).subscribe(repeat => {
            this.extractDataFromAPI(this.result.fetchResult(this.jobId));
          });
        }
      });
    }

    else if (this.type === 'rfr') {

      this.result.randForestRegResult(this.start, this.end,
        this.ticker, this.capitalBase, this.minutes, this.logChannel).subscribe(response => {
          if (!response) {
            alert("Something went wrong!");
          }

          else {
            this.jobId = response.job_id;

            this.log = this.log.concat("Request was queued, please be patient as it runs.", "\n");

            this.subscription = interval(3000).subscribe(repeat => {
              this.extractDataFromAPI(this.result.fetchResult(this.jobId));
            });
          }
      });
    }

    else if (this.type === 'rsi') {

      this.result.rsiDivergenceResult(this.start, this.end, this.ticker,
        this.capitalBase, this.logChannel).subscribe(response => {
          if (!response) {
            alert("Something went wrong!");
          }

          else {
            this.jobId = response.job_id;

            this.log = this.log.concat("Request was queued, please be patient as it runs.", "\n");

            this.subscription = interval(5000).subscribe(repeat => {
              this.extractDataFromAPI(this.result.fetchResult(this.jobId));
            });
          }
      });
    }

    else if (this.type === 'trend') {
      this.result.trendFollowResult(this.start, this.end,
        this.capitalBase, this.logChannel).subscribe(response => {
          if (!response) {
            alert("Something went wrong!");
          }

          else {

            console.log(response);

            this.jobId = response.job_id;

            this.log = this.log.concat("Request was queued, please be patient as it runs.", "\n");

            this.subscription = interval(5000).subscribe(repeat => {
              this.extractDataFromAPI(this.result.fetchResult(this.jobId));
            });
          }
      });
    }
  }

  ngOnDestroy() {
    if (this.subscription !== undefined && this.subscription !== null) {
      this.subscription.unsubscribe();
    }
  }

  public static dateNumToString(num, date: Date) {

    date.setTime(num);

    return date.toDateString().substring(4);
  }

  private static generateRandomString(): string {
    return Math.random().toString(36).substring(2, 15)
      + Math.random().toString(36).substring(2, 15);
  }

  private extractDataFromAPI(observable: Observable<any>) {
    observable.subscribe(response => {

      if (!response) {
        return;
      }

      else if (!response.done) {
        return;
      }

      else {

        this.subscription.unsubscribe();

        let algoToBench = response.algo_to_benchmark;
        let rollingBeta = response.rolling_beta;
        this.finalAlpha = response.alpha;

        let date = new Date();

        let algo = [];
        let bench = [];

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
          beta.push(point[1]);
        }

        this.dataset2.push({
          data: beta,
          label: "Beta"
        });

        this.done = true;

        if (this.ws) {
          this.ws.close();
        }

        this.scroll.scrollTo({
          target: "graph"
        });
      }
    });
  }

}
