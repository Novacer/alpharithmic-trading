import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-intro',
  templateUrl: './intro.component.html',
  styleUrls: ['./intro.component.css']
})
export class IntroComponent implements OnInit {

  public images: string[];

  constructor() {
    this.images = [''];
  }

  ngOnInit() {
  }

}
