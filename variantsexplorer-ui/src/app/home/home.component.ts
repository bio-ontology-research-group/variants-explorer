import { HttpErrorResponse, HttpEventType } from '@angular/common/http';
import { Component, ElementRef, OnInit, ViewChild, QueryList, ViewChildren } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { of } from 'rxjs';  
import { interval } from 'rxjs';
import { catchError, map, startWith } from 'rxjs/operators'; 
import { NgbdSortableHeader, SortEvent } from '../sortable.directive';
import { VariantsExplorerService } from '../variants-explorer.service';

const compare = (v1: string | number, v2: string | number) => v1 < v2 ? -1 : v1 > v2 ? 1 : 0;

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  @ViewChildren(NgbdSortableHeader) headers: QueryList<NgbdSortableHeader>;

  @ViewChild("fileUpload", {static: false}) fileUpload: ElementRef;
  file = null;
  
  uploadForm: FormGroup;

  isCollapsed = true;
  requiredError = "this field is required";
  errorReport = '';
  jobs = [];
  jobsFiltered = [];
  GRCh38 = 'GRCh38';

  page = 1;
  pageSize = 20;
  collectionSize = 0;
  filter = new FormControl('');
  jobLoading = false;
  jobFormLoading = false;

  jobsFilter = (text: string): any[] => {
    return this.jobs.filter(job => {
      const term = text.toLowerCase();
      return job.name.toLowerCase().includes(term) || job.submitted_at.toLowerCase().includes(term);
    });
  }

  constructor(private veSrv: VariantsExplorerService,
    private fb: FormBuilder,
    private route: ActivatedRoute, 
    private router:Router) { }

  ngOnInit(): void {
    this.uploadForm = this.fb.group({
      name: [''],
      content: [''],
      file: [''],
      assembly: [this.GRCh38, Validators.required]
    }, {
      validator: AtleastOneFieldRequired('content', 'file')
    });


    this.filter.valueChanges.pipe(
      startWith(''),
      map(text => this.jobsFilter(text))
    ).subscribe(data => {this.jobs = data;});

    this.findJobs();
    // refresh list after 10 seconds 
    setInterval(() => { 
      if (this.isCollapsed) {
        this.findJobs();
      }
    }, 10000);
  }

  get f() { return this.uploadForm.controls }

  onSubmit() {
    var job = Object.assign({}, this.uploadForm.value);
    delete job['file'];
    // sample['sampleCollectionDate'] = this.toModel(sample['sampleCollectionDate']);

    const formData = new FormData();  
    if (this.file) {
      formData.append('file', this.file);  
      formData.append('filename', this.file.name)
    }
    formData.append('job', JSON.stringify(job))

    var inProgress = true;  
    this.errorReport = '';
    this.jobFormLoading = true;
    this.veSrv.submitJob(formData).pipe(  
      map(event => {  
        switch (event.type) {  
          case HttpEventType.UploadProgress:  
            var progress = Math.round(event.loaded * 100 / event.total);  
            // console.log(progress)
            break;  
          case HttpEventType.Response:  
            return event;  
        }  
      }),  
      catchError((error: HttpErrorResponse) => {  
        inProgress = false;  
        if (error.status == 400){
          console.log(error)
          return of(error['error'].trim());
        }
        this.jobFormLoading = false;
        return of(`${this.file.name} upload failed.`);  
      })).subscribe((event: any) => {  
        if (typeof(event) == 'object' && event.status === 201) {  
          this.reset();
          this.findJobs();
        }  else {
          if (event) {
            this.errorReport = event.split('\n');
          }
        }
        this.jobFormLoading = false;
    }); 

  }
  
  uploadFile(files: FileList) {  
    this.file = files.item(0) 
  }

  onCancel(){
    this.reset()
  }

  reset() {
    this.isCollapsed = true;
    this.uploadForm.reset();
    this.f.assembly.setValue(this.GRCh38);
    this.file = null;
  }

  findJobs(){
    this.jobLoading = true;
    this.veSrv.find().subscribe(res => {
      this.jobs = res
      this.jobLoading = false;
      this.jobsFiltered = this.jobsFilter(this.filter.value);
    });
  }

  delete(jobId) {
    this.veSrv.deleteJob(jobId).subscribe(res => {
      this.findJobs();
    });
  }

  onSort({column, direction}: SortEvent) {
    // resetting other headers
    this.headers.forEach(header => {
      if (header.sortable !== column) {
        header.direction = '';
      }
    });

    if (direction === '' || column === '') {
      this.jobsFiltered = this.jobsFilter(this.filter.value);
    } else {
      this.jobsFiltered = this.jobsFiltered.sort((a, b) => {
        const res = compare(a[column], b[column]);
        return direction === 'asc' ? res : -res;
      });
    }
  }

  example(exampleType) {
    if (exampleType == 'vcf') {
      this.f.content.setValue(`1 818046 . T C . . .
2 265023 . C A . . .
3 361463 . GA G . . .`)
    } else if (exampleType == 'identifiers') {
      this.f.content.setValue(`rs699
rs144678492`)
    } else if (exampleType == 'ensembl') {
      this.f.content.setValue(`1 818046 818046 T/C 1
2 265023 265023 C/A 1
3 361464 361464 A/- 1`)
    } else if (exampleType == 'hgvs') {
      this.f.content.setValue(`AGT:c.803T>C
9:g.22125503G>C
ENST00000003084:c.1431_1433delTTC`)
    }
  }


  get jobPage(): Object[] {
    this.collectionSize = this.jobsFiltered ? this.jobsFiltered.length : 0;
    return this.jobsFiltered ? this.jobsFiltered
      .map((concept, i) => ({id: i + 1, ...concept}))
      .slice((this.page - 1) * this.pageSize, (this.page - 1) * this.pageSize + this.pageSize) : []; 
  }

}


export function AtleastOneFieldRequired(controlName1: string, controlName2: string) {
  return (formGroup: FormGroup) => {
      const control1 = formGroup.controls[controlName1];
      const control2 = formGroup.controls[controlName2];

      if (control2.errors && !control2.errors.atleastOneFieldRequired) {
          // return if another validator has already found an error on the control2
          return;
      }

      // set error on control2 if validation fails
      if (!control1.value && !control2.value) {
        control2.setErrors({ atleastOneFieldRequired: true });
      } else {
        control2.setErrors(null);
      }
  }
}
