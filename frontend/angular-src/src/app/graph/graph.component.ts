import {AfterViewInit, Component, ElementRef, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit {

  constructor(private elementRef: ElementRef) {
  }

  ngOnInit() {
  }

}
