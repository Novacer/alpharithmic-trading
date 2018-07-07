import {AfterViewInit, Component, OnInit, ElementRef} from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  private url: string;
  public algoToBench : any;
  public rollingBeta: any;

  public xaxis : string[];
  public yaxis : number[];

  public done: boolean;

  constructor(private http: HttpClient, private elementRef: ElementRef) {
    this.url = "/api/post/buy-apple";
    this.done = false;

    this.xaxis = [];
    this.yaxis = [];
  }

  ngOnInit() {
    this.doApiCall();
  }

  doApiCall() {

    let body = {
      start: "2015-01-01",
      end: "2016-01-01",
      shares: 50,
      capital_base: 1000000
    };

    this.http.post(this.url, body).subscribe((response: AlgoResponse) => {
      this.algoToBench = response.algo_to_benchmark;
      this.rollingBeta = response.rolling_beta;

      console.log(this.algoToBench);

      let date = new Date();

      for (let point of this.algoToBench.data.data01) {

        this.xaxis.push(this.dateNumToUTC(point[0], date));
        this.yaxis.push(point[1]);
      }

      this.done = true;
    });
  }

  dateNumToUTC(num, date: Date) {

    date.setTime((num - 719529) * 86400000);

    return date.toDateString().substring(4);
  }
}

interface AlgoResponse {
  alpha: number,
  algo_to_benchmark: string,
  rolling_beta: string
}
