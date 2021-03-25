import { Component, Input, OnInit, Output, Directive, EventEmitter, ViewChildren, QueryList, SimpleChange} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { VariantsExplorerService } from '../variants-explorer.service';
import * as _ from 'underscore';
import { NgSelectConfig } from '@ng-select/ng-select';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Location } from "@angular/common";
import { NgbdSortableHeader, SortEvent } from '../sortable.directive';
@Component({
  selector: 'app-variants-details',
  templateUrl: './variants-details.component.html',
  styleUrls: ['./variants-details.component.css']
})
export class VariantsDetailsComponent implements OnInit {
  @ViewChildren(NgbdSortableHeader) sortHeaders: QueryList<NgbdSortableHeader>;

  orderBy = '';
  searchForm : FormGroup;
  job = null;
  variantRecords = null;
  jobId = null;
  fieldConfig = null;
  isCollapsed = true;

  page = 1;
  previousPage = 1;
  pageSize = 20;
  collectionSize = 0;
  queryParams = {};
  searchedTermsObjs=[];
  selectedColumns = [];

  constructor(private veSrv: VariantsExplorerService,
    private route: ActivatedRoute,
    private router: Router,
    public fb: FormBuilder,
    private readonly location: Location,
    private config: NgSelectConfig) { 
      this.config.appendTo = 'body';
      this.veSrv.getConfig().subscribe(res => {
        this.fieldConfig = res
        this.setFormValues();
        this.selectedColumns = _.filter(this.fieldConfig.headers, items => items.hide == false);
      });
  }

  ngOnInit(): void {
    this.searchForm = this.fb.group({
      Consequence: [[]],
      'SIFT_object.term': [[]],
      'PolyPhen_object.term': [[]],
      AFMin: [''],
      AFMax: [''],
    });

    this.route.params.subscribe(params => {
      this.jobId = params.id;
      this.veSrv.getJob(params.id).subscribe(res => {
        this.job = res
      });
      this.findVariantRecords(); 
    });    


    this.route.queryParams.subscribe(params => {
      this.page = 1;
      this.queryParams = Object.assign({}, params);
      // console.log("changed params", this.queryParams)
      this.setSearchLabels();
      this.setFormValues();
      this.findVariantRecords();
    });
  }

  get f() { return this.searchForm.controls }

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
    filter['orderby'] = this.orderBy;
    this.veSrv.findRecords(this.jobId, filter).subscribe(res => {
      this.variantRecords = res['data'] && res['data'].length > 1 ? res['data'] : []; 
      this.collectionSize = res['total'];
      console.log(res)
    });
  }

  onSiftSelect(event) {
    this.setFilters();
    this.navigate();
  }
  
  onConsequenceSelect(event) {
    this.setFilters();
    this.navigate();
  }  

  onPolyphenSelect(event) {
    this.setFilters();
    this.navigate();
  }

  setFilters() {
    this.queryParams = {};
    Object.keys(this.f).forEach(key => {
      if (this.f[key].value) {
        if (key.includes('Min') || key.includes('Max')) {
          let param = key.substring(0, key.length-3);
          let val = key.includes('Min') ? 'ge' + this.f[key].value : 'le' + this.f[key].value;
          if (this.queryParams[param] && this.queryParams[param].length > 0) {
            this.queryParams[param].push(val)
          } else { 
            this.queryParams[param] = [val]
          }

        } else if (Array.isArray(this.f[key].value)) {
          this.queryParams[key] = _.map(this.f[key].value, obj => obj.code);
        } else {
          this.queryParams[key] = this.f[key].value
        }
      } 
    });
  }

  onTermRemoved(key) {
    let params = Object.assign({}, this.queryParams);
    if (key.includes(":")) {
      let keyPart = key.split(":")[0]
      if (params[keyPart].length > 1) {
        var index = params[keyPart].indexOf(key.split(":")[1]);
        if (index !== -1) {
          params[keyPart].splice(index, 1);
        }
      } else {
        delete params[keyPart];
      }
    } else {
      delete params[key];
    }
    this.queryParams = params;
    this.navigate();
  }

  clearFilters() {
    this.queryParams={};
    this.searchedTermsObjs=[];
    this.navigate();
  }

  setFormValues(){
    let formVal = {
      Consequence: [],
      'SIFT_object.term': [],
      'PolyPhen_object.term': [],
      AFMin: '',
      AFMax: '',
    };
    Object.keys(this.queryParams).forEach(val => {
      if (Array.isArray(this.queryParams[val])) {
        this.queryParams[val].forEach(item => {
          this.setValue(val, item, formVal);
        });
      } else {
        this.setValue(val, this.queryParams[val], formVal);
      }
    });
    // console.log(this.queryParams,formVal)
    this.searchForm.setValue(formVal);
  }

  setValue(key, value, formObj){
    if (value.substring(0,2) == 'le') {
      formObj[key + 'Max'] = value.substring(2, value.length);
    } else if (value.substring(0,2) == 'ge') {
      formObj[key + 'Min'] = value.substring(2, value.length);
    } else {
      if (this.fieldConfig && this.fieldConfig[key.split('_')[0]]) {
        let codeObj = _.findWhere(this.fieldConfig[key.split('_')[0]], {"code" : value});
        formObj[key].push(codeObj ? codeObj:value);
      }
    }
  }

  setSearchLabels() {
    this.searchedTermsObjs = [];
    Object.keys(this.queryParams).forEach(val => {
      if (Array.isArray(this.queryParams[val])) {
        this.queryParams[val].forEach(item => {
          this.searchedTermsObjs.push({'key':val + ":" + item, 'value':item});
        });
      } else {
        this.searchedTermsObjs.push({'key':val, 'value':this.queryParams[val]});
      }
    });
  }

  onHeadersSelect(event) {
    console.log(this.selectedColumns);
    
  }

  onSort({column, direction}: SortEvent) {
    // resetting other headers
    this.sortHeaders.forEach(header => {
      if (header.sortable !== column) {
        header.direction = '';
      }
    });

    // sorting countries
    if (direction === '' || column === '') {
      this.orderBy = '';
    } else {
      this.orderBy = column + ":" + direction;
    }
    this.findVariantRecords()
  }

  navigate() {
    this.page = 1;
    this.setFormValues();
    const urlTree = this.router.createUrlTree([], {relativeTo:this.route, queryParams: this.queryParams});
    this.location.go(urlTree.toString()); 
    this.findVariantRecords();
    this.setSearchLabels();
  }

}
