import { Injectable } from '@angular/core';
import {Observable} from "rxjs/internal/Observable";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class ResultService {

  private readonly buyAppleURL : string;
  private readonly meanReversionURL : string;

  constructor(private http: HttpClient) {
    this.buyAppleURL = "/api/post/buy-apple";
    this.meanReversionURL = "/api/post/mean-reversion"
  }

  /**
   * Returns an Observable with the result of buying Apple Shares everyday
   * @param {string} start the start date (in YYYY-MM-DD)
   * @param {string} end the end date (in YYYY-MM-DD)
   * @param {number} shares the number of shares to buy each day
   * @param {number} capitalBase the total amount of money you have
   * @param {string} logChannel the channel for which logs will be pushed to
   */
  buyAppleResult(start: string, end: string,
                 shares: number, capitalBase: number,
                 logChannel: string) : Observable<any> {

    let body = {
      start: start,
      end: end,
      shares: shares,
      capital_base: capitalBase,
      log_channel: logChannel
    };

    return this.http.post(this.buyAppleURL, body);
  }


  meanReversionResult(start: string, end: string,
                      shares: number, capitalBase: number,
                      logChannel: string) :Observable<any> {

    let body = {
      start: start,
      end: end,
      shares: shares,
      capital_base: capitalBase,
      log_channel: logChannel
    };

    return this.http.post(this.meanReversionURL, body);
  }
}
