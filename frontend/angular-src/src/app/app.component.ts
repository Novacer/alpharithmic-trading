import {AfterViewInit, Component, OnInit, ElementRef} from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {

  private url: string;
  public algoToBench : string;
  public rollingBeta: string;

  public done: boolean;

  constructor(private http: HttpClient, private elementRef: ElementRef) {
    this.url = "/api/post/buy-apple";
    this.done = false;
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

      this.algoToBench = this.algoToBench.slice(this.algoToBench.indexOf("!f"), this.algoToBench.lastIndexOf("</"));
      this.done = true;
    });
  }
}

interface AlgoResponse {
  alpha: number,
  algo_to_benchmark: string,
  rolling_beta: string
}
