import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {ScrollToService} from '@nicky-lenaers/ngx-scroll-to';
import {ValidateResponse, ValidationService} from '../../services/validation.service';
import {MatSnackBar} from '@angular/material';

@Component({
  selector: 'app-rand-forest-reg',
  templateUrl: './rand-forest-reg.component.html',
  styleUrls: ['./rand-forest-reg.component.css']
})
export class RandForestRegComponent implements OnInit {

  firstForm: FormGroup;
  secondForm: FormGroup;
  thirdForm: FormGroup;

  startDate: FormControl;
  endDate: FormControl;

  capitalBase: number;
  ticker: string;
  minutesAfterOpen: number;

  beginSim: boolean;
  validating: boolean;

  constructor(private formBuilder: FormBuilder, private scroll: ScrollToService,
              private validation: ValidationService, private snackBar: MatSnackBar) {
  }

  ngOnInit() {

    this.scroll.scrollTo({
      target: 'top'
    });

    this.firstForm = this.formBuilder.group({firstCtrl: ['', Validators.required]});
    this.secondForm = this.formBuilder.group({secondCtrl: ['', Validators.required]});
    this.thirdForm = this.formBuilder.group({thirdCtrl: ['', Validators.required]});

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
    this.ticker = '';
    this.minutesAfterOpen = 1;
    this.beginSim = false;
    this.validating = false;
  }

  onDoneClick() {

    this.validating = true;

    this.validation.validateSymbol(this.ticker).subscribe((response: ValidateResponse) => {
      if (response && response.success) {
        this.scroll.scrollTo({
          target: 'results'
        });

        this.validating = false;
        this.beginSim = true;
      } else {
        this.snackBar.open('Oops! We don\'t have your chosen stock in our database!',
          'Pick another one', {
            duration: 10000
          });

        this.validating = false;
      }
    });

  }

  onResetClick() {
    this.beginSim = false;
  }

  static getDate(form: FormControl) {
    return form.value.toISOString().substring(0, 10);
  }

}
