import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs/internal/Observable';
import {map} from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class EditorService {

  private readonly defaultSrcURL = '/api/get/default-src-code';

  constructor(private http: HttpClient) { }

  getDefaultSrcCode(): Observable<string> {
    return this.http.get(this.defaultSrcURL).pipe(
      map((response: DefaultSrcResponse) => response.code)
    );
  }
}

interface DefaultSrcResponse {
  code: string;
}
