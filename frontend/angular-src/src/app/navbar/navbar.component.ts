import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {

  constructor() {
  }

  ngOnInit() {
  }

  onLearnMoreClick() {
    window.location.href = 'https://github.com/Novacer/alpharithmic-trading#alpharithmic-trading';
  }

}
