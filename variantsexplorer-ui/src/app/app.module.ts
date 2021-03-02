import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HelpComponent } from './help/help.component';
import { HomeComponent } from './home/home.component';
import { HttpClientModule } from '@angular/common/http';
import { UploadFormComponent } from './upload-form/upload-form.component';
import { VariantsDetailsComponent } from './variants-details/variants-details.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { VariantsExplorerService } from './variants-explorer.service';

@NgModule({
  declarations: [
    AppComponent,
    HelpComponent,
    HomeComponent,
    UploadFormComponent,
    VariantsDetailsComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    NgbModule,
    AppRoutingModule
  ],
  providers: [VariantsExplorerService],
  bootstrap: [AppComponent]
})
export class AppModule { }
