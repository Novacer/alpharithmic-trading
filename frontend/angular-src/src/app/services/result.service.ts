import { Injectable } from '@angular/core';
import {Observable} from "rxjs/internal/Observable";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class ResultService {

  private readonly buyAppleURL : string;
  private readonly meanReversionURL : string;
  private readonly randForestRegURL : string;
  private readonly rsiDivergenceURL : string;
  private readonly trendFollowURL : string;
  private readonly fetchResultURL : string;
  private readonly regimesClusteringURL: string;

  constructor(private http: HttpClient) {
    this.buyAppleURL = "/api/post/buy-apple";
    this.meanReversionURL = "/api/post/mean-reversion";
    this.randForestRegURL = "/api/post/random-forest-regression";
    this.rsiDivergenceURL = "/api/post/rsi-divergence";
    this.trendFollowURL = "/api/post/trend-follow";
    this.regimesClusteringURL = "/api/post/regimes-clustering";
    this.fetchResultURL = "/api/post/result";
  }

  /**
   * Returns an Observable with the job_id of buying Apple Shares everyday
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


  /**
   * Returns an Observable with the job_id of the Mean Reversion simulation
   * @param {string} start the simulation start date
   * @param {string} end the simulation end date
   * @param {number} shares the number of shares to buy each time
   * @param {number} capitalBase the initial capital base
   * @param {string} logChannel the channel which logs will be pushed to
   * @returns {Observable<any>}
   */
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


  /**
   * returns an Observable with the job_id of the Random Forest Regression simulation
   * @param {string} start the simulation start date
   * @param {string} end the simulation end date
   * @param {string} ticker the stock ticker to trade
   * @param {number} capitalBase the initial capital base
   * @param {number} minutes the minutes after market open to execute the trade
   * @param {string} logChannel the channel for which logs are pushed to
   * @returns {Observable<any>}
   */
  randForestRegResult(start: string, end: string,
                      ticker: string, capitalBase: number,
                      minutes: number, logChannel: string) : Observable<any> {

    let body = {
      start: start,
      end: end,
      ticker: ticker,
      minutes: minutes,
      capital_base: capitalBase,
      log_channel: logChannel
    };

    return this.http.post(this.randForestRegURL, body);
  }

  /**
   * returns an Observable with the job_id of the RSI Divergence simulation
   * @param {string} start the simulation start date
   * @param {string} end the simulation end date
   * @param {string} ticker the stock's ticker
   * @param {number} capitalBase the initial capital base
   * @param {string} logChannel the channel for which logs are pushed to
   * @returns {Observable<any>}
   */
  rsiDivergenceResult(start: string, end: string,
                      ticker: string, capitalBase: number,
                      logChannel: string) : Observable<any>{

    let body = {
      start: start,
      end: end,
      ticker: ticker,
      capital_base: capitalBase,
      log_channel: logChannel
    };

    return this.http.post(this.rsiDivergenceURL, body);
  }


  /**
   * returns an Observable with the job_id of the Trend Follow simulation
   * @param {string} start the start date
   * @param {string} end the simulation end date
   * @param {number} capitalBase the initial capital base
   * @param {string} logChannel the channel for which logs are pushed to
   * @returns {Observable<any>}
   */
  trendFollowResult(start: string, end: string,
                    capitalBase: number, logChannel: string) : Observable<any> {

    let body = {
      start: start,
      end: end,
      capital_base: capitalBase,
      log_channel: logChannel
    };

    return this.http.post(this.trendFollowURL, body);
  }

  /**
   * returns an Observable with the job_id of the Regimes Clustering simulation
   * @param {string} start the start date
   * @param {string} end the simulation end date
   * @param {string} ticker the stock ticker to trade
   * @param {number} capitalBase the initial capital base
   * @param {boolean} useClf use random forest classifier instead of regressor
   * @param {boolean} noShorts disable shorting
   * @param {string} logChannel the channel for which logs are pushed to
   * @returns {Observable<any>}
   */
  regimesClusteringResult(start: string, end: string, ticker: string,
                          capitalBase: number, useClf: boolean, noShorts: boolean,
                          logChannel: string) : Observable<any>{

    let body = {
      start: start,
      end: end,
      ticker: ticker,
      use_clf: useClf,
      no_shorts: noShorts,
      capital_base: capitalBase,
      log_channel: logChannel
    };

    return this.http.post(this.regimesClusteringURL, body);
  }

  /**
   * Returns an Observable with the result of the job with job_id. The job may or may not be finished
   * @param {string} jobId the job_id
   * @returns {Observable<Object>}
   */
  fetchResult(jobId : string) {

    let body = {
      job_id: jobId.substring(7)
    };

    return this.http.post(this.fetchResultURL, body);
  }
}
