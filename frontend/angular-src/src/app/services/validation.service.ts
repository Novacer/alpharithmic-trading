import { Injectable } from '@angular/core';
import {HttpClient, HttpParams} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class ValidationService {

  private readonly validateSymbolURL = "/api/get/validate-symbol";

  constructor(private http: HttpClient) { }

  validateSymbol(symbol : string) {

    let httpParams = new HttpParams().append("symbol", symbol);

    return this.http.get(this.validateSymbolURL, {params: httpParams});
  }
}
