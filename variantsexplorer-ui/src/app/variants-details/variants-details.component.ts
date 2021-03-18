import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { VariantsExplorerService } from '../variants-explorer.service';
import * as _ from 'underscore';
import { NgSelectConfig } from '@ng-select/ng-select';
import { FormControl } from '@angular/forms';
@Component({
  selector: 'app-variants-details',
  templateUrl: './variants-details.component.html',
  styleUrls: ['./variants-details.component.css']
})
export class VariantsDetailsComponent implements OnInit {
  job = null;
  variantRecords = null;
  jobId = null;
  fieldConfig = null;
  isCollapsed = true;

  page = 1;
  previousPage = 1;
  pageSize = 20;
  collectionSize = 0;
  consequenceFilter = [];
  siftFilter = '';
  polyphenFilter = '';
  queryParams = {};


  afMinFilter = new FormControl('');
  afMaxFilter = new FormControl('');
  siftMinFilter = new FormControl('');
  siftMaxFilter = new FormControl('');
  polyPhenMinFilter = new FormControl('');
  polyPhenMaxFilter = new FormControl('');

  constructor(private veSrv: VariantsExplorerService,
    private route: ActivatedRoute,
    private router: Router,
    private config: NgSelectConfig) { 
    this.config.appendTo = 'body';
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.jobId = params.id;
      this.veSrv.getJob(params.id).subscribe(res => {
        this.job = res
      });
      this.veSrv.getConfig().subscribe(res => {
        this.fieldConfig = res
      })
      this.findVariantRecords();
    });    


    this.route.queryParams.subscribe(params => {
      this.page = 1;
      console.log(params)
      this.queryParams = Object.assign({}, params);
      this.findVariantRecords();
    });
  }

  loadPage(page: number) {
    if (page !== this.previousPage) {
      this.previousPage = page;
      this.findVariantRecords();
    }
  }

  onPageSizeChange(event){
    this.page = 1;
    this.findVariantRecords();
  }

  findVariantRecords() {
    var offset = 0
    if (this.page > 1) {
      offset = this.pageSize * (this.page - 1)
    }
    
    let filter = Object.assign({}, this.queryParams)
    filter['limit'] = this.pageSize;
    filter['offset'] = offset;
    this.veSrv.findRecords(this.jobId, filter).subscribe(res => {
      this.variantRecords = res['data'] && res['data'].length > 1 ? res['data'] : []; 
      this.collectionSize = res['total'];
      console.log(res)
    });
  }

  onSiftSelect(event) {
    this.queryParams['SIFT_object.term'] = event.target.value;
    this.router.navigate(['/job', this.jobId], { queryParams: this.queryParams});
  }
  
  onConsequenceSelect(event) {
    this.queryParams['Consequence'] = _.map(event, obj => obj.code);
    this.router.navigate(['/job', this.jobId], { queryParams: this.queryParams});
  }

  onPolyphenSelect(event) {
    console.log( event.target.value, this.queryParams)
    this.queryParams['PolyPhen_object.term'] = event.target.value;
    this.router.navigate(['/job', this.jobId], { queryParams: this.queryParams});
  }

  setFilters() {
    this.queryParams['AF'] = []
    if (this.afMinFilter.value) { 
      this.queryParams['AF'].push('ge' + this.afMinFilter.value)
    }
    if (this.afMaxFilter.value) { 
      this.queryParams['AF'].push('le' + this.afMaxFilter.value)
    }

    this.queryParams['SIFT_object.score'] = []
    if (this.siftMinFilter.value) { 
      this.queryParams['SIFT_object.score'].push('ge' + this.siftMinFilter.value)
    }
    if (this.siftMaxFilter.value) { 
      this.queryParams['SIFT_object.score'].push('le' + this.siftMaxFilter.value)
    }

    this.queryParams['PolyPhen_object.score'] = []
    if (this.polyPhenMinFilter.value) { 
      this.queryParams['PolyPhen_object.score'].push('ge' + this.polyPhenMinFilter.value)
    }
    if (this.polyPhenMaxFilter.value) { 
      this.queryParams['PolyPhen_object.score'].push('le' + this.polyPhenMaxFilter.value)
    }
    this.router.navigate(['/job', this.jobId], { queryParams: this.queryParams});
  }

}
