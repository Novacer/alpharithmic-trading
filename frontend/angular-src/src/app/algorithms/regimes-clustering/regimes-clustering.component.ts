import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {ScrollToService} from "@nicky-lenaers/ngx-scroll-to";
import {ValidateResponse, ValidationService} from "../../services/validation.service";
import {MatSnackBar} from "@angular/material";

@Component({
  selector: 'app-regimes-clustering',
  templateUrl: './regimes-clustering.component.html',
  styleUrls: ['./regimes-clustering.component.css']
})
export class RegimesClusteringComponent implements OnInit {

  public firstForm : FormGroup;
  public secondForm : FormGroup;
  public thirdForm : FormGroup;

  public startDate : FormControl;
  public endDate : FormControl;

  public capitalBase : number;
  public ticker : string;
  public noShorts : boolean;
  public useClf : boolean;

  public beginSim : boolean;
  public validating : boolean;

  constructor(private formBuilder: FormBuilder, private scroll: ScrollToService,
              private validation: ValidationService, private snackBar: MatSnackBar) { }

  ngOnInit() {

    this.scroll.scrollTo({
      target: 'top'
    });

    this.firstForm =  this.formBuilder.group({firstCtrl: ['', Validators.required]});
    this.secondForm = this.formBuilder.group({secondCtrl: ['', Validators.required]});
    this.thirdForm = this.formBuilder.group({thirdCtrl: ['', Validators.required]});

    let start = new Date();
    start.setFullYear(2017);
    start.setMonth(3);
    start.setDate(1);

    this.startDate = new FormControl(start);

    let end = new Date();
    end.setFullYear(2018);
    end.setMonth(3);
    end.setDate(1);

    this.endDate = new FormControl(end);

    this.capitalBase = 1000000;
    this.ticker = "";

    this.noShorts = false;
    this.useClf = true;

    this.beginSim = false;
    this.validating = false;
  }

  onDoneClick() {

    this.validating = true;

    this.validation.validateSymbol(this.ticker).subscribe((response : ValidateResponse) => {
      if (response && response.success) {
        this.scroll.scrollTo({
          target: "results"
        });

        this.validating = false;
        this.beginSim = true;
      }

      else {
        this.snackBar.open("Oops! We don't have your chosen stock in our database!",
          "Pick another one", {
            duration: 10000
          });

        this.validating = false;
      }
    });

  }

  onResetClick() {
    this.beginSim = false;
  }

  getDate(form: FormControl) {
    return form.value.toISOString().substring(0, 10);
  }

}
