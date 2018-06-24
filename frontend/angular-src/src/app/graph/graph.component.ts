import {AfterViewInit, Component, ElementRef, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.css']
})
export class GraphComponent implements OnInit, AfterViewInit {

  @Input()
  public html : string;

  constructor(private elementRef: ElementRef) {
  }

  ngOnInit() {
  }

  ngAfterViewInit() {
    this.loadScript("https://mpld3.github.io/js/d3.v3.min.js").then(data => {
      this.loadScript("https://mpld3.github.io/js/mpld3.v0.3.js").then(data => {

        var s = document.createElement("script");
        s.type = "text/javascript";
        s.innerHTML = this.html;
        this.elementRef.nativeElement.appendChild(s);
      });
    });
  }

  private loadScript(scriptUrl: string) {
    return new Promise((resolve, reject) => {
      const scriptElement = document.createElement('script');
      scriptElement.type = "text/javascript";
      scriptElement.src = scriptUrl;
      scriptElement.onload = resolve;
      scriptElement.charset = "utf-8";
      this.elementRef.nativeElement.appendChild(scriptElement);

      resolve();
    })
  }

}
