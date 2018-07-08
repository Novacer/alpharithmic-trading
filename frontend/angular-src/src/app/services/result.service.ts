import { Injectable } from '@angular/core';
import {Observable} from "rxjs/internal/Observable";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class ResultService {

  private buyAppleURL : string;

  constructor(private http: HttpClient) {
    this.buyAppleURL = "/api/post/buy-apple";
  }

  /**
   * Returns an Observable with the result of buying Apple Shares everyday
   * @param {string} start the start date (in YYYY-MM-DD)
   * @param {string} end the end date (in YYYY-MM-DD)
   * @param {number} shares the number of shares to buy each day
   * @param {number} capitalBase the total amount of money you have
   */
  buyAppleResult(start: string, end: string, shares: number, capitalBase: number) : Observable<any> {

    let body = {
      start: start,
      end: end,
      shares: shares,
      capital_base: capitalBase
    };

    return this.http.post(this.buyAppleURL, body);
  }
}
