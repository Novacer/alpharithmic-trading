import {AfterViewInit, Component, OnInit, ElementRef} from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {


  constructor() {
  }

  ngOnInit() {
  }
}

interface AlgoResponse {
  alpha: number,
  algo_to_benchmark: string,
  rolling_beta: string
}
