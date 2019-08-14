import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {ScrollToService} from '@nicky-lenaers/ngx-scroll-to';

@Component({
  selector: 'app-trend-follow',
  templateUrl: './trend-follow.component.html',
  styleUrls: ['./trend-follow.component.css']
})
export class TrendFollowComponent implements OnInit {

  firstForm: FormGroup;
  secondForm: FormGroup;

  startDate: FormControl;
  endDate: FormControl;

  capitalBase: number;

  beginSim: boolean;

  constructor(private formBuilder: FormBuilder, private scroll: ScrollToService) {
  }

  ngOnInit() {

    this.scroll.scrollTo({
      target: 'top'
    });

    this.firstForm = this.formBuilder.group({firstCtrl: ['', Validators.required]});
    this.secondForm = this.formBuilder.group({secondCtrl: ['', Validators.required]});

    const start = new Date();
    start.setFullYear(2017);
    start.setMonth(3);
    start.setDate(1);

    this.startDate = new FormControl(start);

    const end = new Date();
    end.setFullYear(2018);
    end.setMonth(3);
    end.setDate(1);

    this.endDate = new FormControl(end);

    this.capitalBase = 1000000;
    this.beginSim = false;
  }

  onDoneClick() {

    this.scroll.scrollTo({
      target: 'results'
    });
    this.beginSim = true;

  }

  onResetClick() {
    this.beginSim = false;
  }

  static getDate(form: FormControl) {
    return form.value.toISOString().substring(0, 10);
  }
}
