import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {ScrollToService} from "@nicky-lenaers/ngx-scroll-to";

@Component({
  selector: 'app-buy-apple',
  templateUrl: './buy-apple.component.html',
  styleUrls: ['./buy-apple.component.css']
})
export class BuyAppleComponent implements OnInit {

  public firstForm : FormGroup;
  public secondForm : FormGroup;
  public thirdForm : FormGroup;

  public startDate : FormControl;
  public endDate : FormControl;

  public capitalBase : number;
  public numOfShares : number;

  public beginSim : boolean;

  constructor(private formBuilder: FormBuilder, private scroll: ScrollToService) { }

  ngOnInit() {
    this.firstForm =  this.formBuilder.group({firstCtrl: ['', Validators.required]});
    this.secondForm = this.formBuilder.group({secondCtrl: ['', Validators.required]});
    this.thirdForm = this.formBuilder.group({thirdCtrl: ['', Validators.required]});

    let today = new Date();
    today.setFullYear(today.getFullYear() - 1);

    this.startDate = new FormControl(today);
    this.endDate = new FormControl(new Date());

    this.capitalBase = 1000000;
    this.numOfShares = 50;
    this.beginSim = false;
  }

  onDoneClick() {

    this.scroll.scrollTo({
      target: "results"
    });
    this.beginSim = true;

  }

  getDate(form: FormControl) {
    return form.value.toISOString().substring(0, 10);
  }

}
