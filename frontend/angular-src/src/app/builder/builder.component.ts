import { Component, OnInit } from '@angular/core';
import {ScrollToService} from "@nicky-lenaers/ngx-scroll-to";

@Component({
  selector: 'app-builder',
  templateUrl: './builder.component.html',
  styleUrls: ['./builder.component.css']
})
export class BuilderComponent implements OnInit {

  code = '';

  disableBtn = false;
  beginSim = false;

  constructor(private scroll: ScrollToService) { }

  ngOnInit() {
    this.scroll.scrollTo({
      target: 'top'
    });
  }

  updateCode(newCode: string) {
    this.code = newCode;
    this.beginSim = false;
    this.disableBtn = false;
  }

  sendCodeToCompile() {

    this.scroll.scrollTo({
      target: 'results'
    });

    this.beginSim = true;
    this.disableBtn = true;
  }
}
