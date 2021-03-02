import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HelpComponent } from './help/help.component';
import { HomeComponent } from './home/home.component';
import { UploadFormComponent } from './upload-form/upload-form.component';
import { VariantsDetailsComponent } from './variants-details/variants-details.component';

const routes: Routes = [
  {path: '', component: HomeComponent}, 
  {path: 'upload',component: UploadFormComponent},
  {path: 'job/:id',component: VariantsDetailsComponent},
  {path: 'help',component: HelpComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
