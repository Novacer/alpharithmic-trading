import {Component, OnInit} from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{

  private url : string;

  constructor(private http: HttpClient) {
    this.url = "/api/post/buy-apple"
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

    this.http.post(this.url, body).subscribe(response => {
      console.log(response);
    });
  }
}
