import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-builder',
  templateUrl: './builder.component.html',
  styleUrls: ['./builder.component.css']
})
export class BuilderComponent implements OnInit {

  code = '';

  disableBtn = false;
  beginSim = false;

  constructor() { }

  ngOnInit() {
  }

  updateCode(newCode: string) {
    this.code = newCode;
    this.beginSim = false;
    this.disableBtn = false;
  }

  sendCodeToCompile() {
    this.beginSim = true;
    this.disableBtn = true;
  }
}
