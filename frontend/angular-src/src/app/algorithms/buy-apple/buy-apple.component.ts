import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";

@Component({
  selector: 'app-buy-apple',
  templateUrl: './buy-apple.component.html',
  styleUrls: ['./buy-apple.component.css']
})
export class BuyAppleComponent implements OnInit {

  public firstForm : FormGroup;
  public secondForm : FormGroup;

  public startDate : FormControl;
  public endDate : FormControl;

  public capitalBase : number;

  constructor(private formBuilder: FormBuilder) { }

  ngOnInit() {
    this.firstForm =  this.formBuilder.group({firstCtrl: ['', Validators.required]});
    this.secondForm = this.formBuilder.group({secondCtrl: ['', Validators.required]});

    let today = new Date();
    today.setFullYear(today.getFullYear() - 1);

    this.startDate = new FormControl(today);
    this.endDate = new FormControl(new Date());

    this.capitalBase = 1000000;
  }



}
