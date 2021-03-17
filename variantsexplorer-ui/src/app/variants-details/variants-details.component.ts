import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
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


  afMinFilter = new FormControl('');
  afMaxFilter = new FormControl('');
  siftMinFilter = new FormControl('');
  siftMaxFilter = new FormControl('');
  polyPhenMinFilter = new FormControl('');
  polyPhenMaxFilter = new FormControl('');

  constructor(private veSrv: VariantsExplorerService,
    private route: ActivatedRoute,
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
        console.log(res)
      })
      this.findVariantRecords();
    });    
  }

  loadPage(page: number) {
    if (page !== this.previousPage) {
      this.previousPage = page;
      this.findVariantRecords();
    }
  }

  findVariantRecords() {
    var offset = 0
    if (this.page > 1) {
      offset = this.pageSize * (this.page - 1)
    }
    
    let filter = this.makeFilterObj(offset);
    this.veSrv.findRecords(this.jobId, filter).subscribe(res => {
      this.variantRecords = res['data'] && res['data'].length > 1 ? res['data'] : []; 
      this.collectionSize = res['total'];
      console.log(res)
    });
  }

  makeFilterObj(offset) {
    let filter = {'limit': this.pageSize, 'offset': offset}
    if (this.consequenceFilter && this.consequenceFilter.length > 0) {
      filter['Consequence'] = this.consequenceFilter
    }

    if (this.siftFilter) {
      filter['SIFT_object.term'] = this.siftFilter
    }

    if (this.polyphenFilter) {
      filter['PolyPhen_object.term'] = this.polyphenFilter
    }

    filter['AF'] = []
    if (this.afMinFilter.value) { 
      filter['AF'].push('ge' + this.afMinFilter.value)
    }
    if (this.afMaxFilter.value) { 
      filter['AF'].push('le' + this.afMaxFilter.value)
    }

    filter['SIFT_object.score'] = []
    if (this.siftMinFilter.value) { 
      filter['SIFT_object.score'].push('ge' + this.siftMinFilter.value)
    }
    if (this.siftMaxFilter.value) { 
      filter['SIFT_object.score'].push('le' + this.siftMaxFilter.value)
    }

    filter['PolyPhen_object.score'] = []
    if (this.polyPhenMinFilter.value) { 
      filter['PolyPhen_object.score'].push('ge' + this.polyPhenMinFilter.value)
    }
    if (this.polyPhenMaxFilter.value) { 
      filter['PolyPhen_object.score'].push('le' + this.polyPhenMaxFilter.value)
    }
    return filter;
  }

  onSiftSelect(event) {
    this.siftFilter = event.target.value;
    this.findVariantRecords();
  }
  
  onConsequenceSelect(event) {
    this.consequenceFilter = _.map(event, obj => obj.code);
    this.findVariantRecords();
  }

  onPolyphenSelect(event) {
    this.polyphenFilter = event.target.value;
    this.findVariantRecords();
  }

}
