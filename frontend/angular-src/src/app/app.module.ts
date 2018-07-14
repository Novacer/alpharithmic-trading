import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { HttpClientModule } from "@angular/common/http";
import { GraphComponent } from './graph/graph.component';
import { ChartsModule } from "ng2-charts";
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NavbarComponent } from './navbar/navbar.component'
import { Routes, RouterModule } from "@angular/router";
import { IntroComponent } from './intro/intro.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";
import {
  MatDatepickerModule,
  MatFormFieldModule, MatIconModule, MatInputModule,
  MatNativeDateModule, MatSliderModule,
  MatStepperModule,
  MatToolbarModule
} from "@angular/material";
import { MatButtonModule } from "@angular/material/button";
import { SelectAlgoComponent } from './select-algo/select-algo.component';
import { BuyAppleComponent } from './algorithms/buy-apple/buy-apple.component';
import {ScrollToModule} from "@nicky-lenaers/ngx-scroll-to";
import { MeanReversionComponent } from './algorithms/mean-reversion/mean-reversion.component';

const appRoutes : Routes = [
  { path: '', component: IntroComponent, pathMatch: 'full'},
  { path: 'algorithms', component: SelectAlgoComponent },
  { path: 'algorithms/buy-apple', component: BuyAppleComponent },
  { path: '**', redirectTo: '' }
];

@NgModule({
  declarations: [
    AppComponent,
    GraphComponent,
    NavbarComponent,
    IntroComponent,
    SelectAlgoComponent,
    BuyAppleComponent,
    MeanReversionComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    ChartsModule,
    FormsModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    MatToolbarModule,
    MatButtonModule,
    MatStepperModule,
    MatDatepickerModule,
    MatFormFieldModule,
    MatNativeDateModule,
    MatInputModule,
    MatSliderModule,
    MatIconModule,
    NgbModule.forRoot(),
    ScrollToModule.forRoot(),
    RouterModule.forRoot(appRoutes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
