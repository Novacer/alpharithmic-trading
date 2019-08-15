import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs/internal/Observable';
import {map} from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class EditorService {

  private readonly defaultSrcURL = '/api/get/default-src-code';
  private readonly executeCodeURL = '/api/post/src-code';

  constructor(private http: HttpClient) { }

  getDefaultSrcCode(): Observable<string> {
    return this.http.get(this.defaultSrcURL).pipe(
      map((response: DefaultSrcResponse) => response.code)
    );
  }

  executeSrcCode(code: string, capital_base: number, start: string, end: string, log_channel: string): Observable<object>{
    const body = {
      src_code: code,
      capital_base: capital_base,
      start: start,
      end: end,
      log_channel: log_channel
    };

    return this.http.post(this.executeCodeURL, body);
  }
}

interface DefaultSrcResponse {
  code: string;
}
