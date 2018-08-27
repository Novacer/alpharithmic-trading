import { Component, OnInit } from '@angular/core';
import {ScrollToService} from "@nicky-lenaers/ngx-scroll-to";

@Component({
  selector: 'app-select-algo',
  templateUrl: './select-algo.component.html',
  styleUrls: ['./select-algo.component.css']
})
export class SelectAlgoComponent implements OnInit {

  constructor(private scroll: ScrollToService) {
  }

  ngOnInit() {
    this.scroll.scrollTo({
      target: 'top'
    });
  }

}
