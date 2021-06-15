import { Component, Input, OnInit, Output, Directive, EventEmitter, ViewChildren, QueryList, SimpleChange} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { VariantsExplorerService } from '../variants-explorer.service';
import * as _ from 'underscore';
import { NgSelectConfig } from '@ng-select/ng-select';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Location } from "@angular/common";
import { NgbdSortableHeader, SortEvent } from '../sortable.directive';
import { concat, Observable, of, Subject  } from 'rxjs';
import { catchError, debounceTime, distinctUntilChanged, switchMap, tap } from 'rxjs/operators'
import { LookupService } from '../lookup.service';
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

  phenotype$ : Observable<any>;
  phenotypeLoading = false;
  phenotypeInput$ = new Subject<string>();
  phenotypeNeigborhood = null; 

  goCache = {};
  hpCache = {};

  recordLoading = false;

  constructor(private veSrv: VariantsExplorerService,
    private route: ActivatedRoute,
    private router: Router,
    public fb: FormBuilder,
    private readonly location: Location,
    private lookupSrv: LookupService,
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
      ClinSig:[[]],
      'SIFT_object.term': [[]],
      'PolyPhen_object.term': [[]],
      AFMin: [''],
      AFMax: [''],
      'ontology_filter' : [null] 
    });

    this.route.params.subscribe(params => {
      this.jobId = params.id;
      this.veSrv.getJob(params.id).subscribe(res => {
        this.job = res
        if (this.job.status != 'Done') {
          this.isCollapsed = false;
        } else {
          this.isCollapsed = true;
        }
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
      this.initPhenotypeFilter();
    });
    this.loadPhenotype();
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
    
    this.recordLoading = true;
    let filter = Object.assign({}, this.queryParams)
    filter['limit'] = this.pageSize;
    filter['offset'] = offset;
    filter['orderby'] = this.orderBy;
    this.veSrv.findRecords(this.jobId, filter).subscribe(res => {
      this.variantRecords = res['data'] && res['data'].length > 1 ? res['data'] : []; 
      this.collectionSize = res['total'];

      let goClasses = this.variantRecords.map(record => record['GO_CLASSES']).flat();
      let hpClasses = this.variantRecords.map(record => record['PHENOTYPE']).flat();
      this.resolveOntologyClasses(goClasses, hpClasses);

      this.recordLoading = false;
      this.variantRecords.forEach(element => {
        element['GO_CLASSES_temp'] = {};
        element['GO_CLASSES_temp']['truncated'] = element['GO_CLASSES'].slice(0,2);
        element['GO_CLASSES_temp']['seeLess'] = true;
        element['GO_CLASSES_temp']['full'] = element['GO_CLASSES']


        element['PHENOTYPE_temp'] = {};
        element['PHENOTYPE_temp']['truncated'] = element['PHENOTYPE'].slice(0,2);
        element['PHENOTYPE_temp']['seeLess'] = true;
        element['PHENOTYPE_temp']['full'] = element['PHENOTYPE']

        element['ppiSeeLess']=true;
      });
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

  onClinicalSigSelect(event) {
    this.setFilters();
    this.navigate();
  }  

  onPolyphenSelect(event) {
    this.setFilters();
    this.navigate();
  }
  
  onPhenotypeSelect(event) {
    console.log(event);
    this.setFilters();
    this.navigate();
  }

  onPhenotypeBtn(hpClass) {
    hpClass = hpClass.split('/').pop().replace('_',':');
    this.f['ontology_filter'].setValue(hpClass);
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
          this.queryParams[key] = _.map(this.f[key].value, obj => obj['code'] ? obj.code : obj.class);
        }  else if (typeof this.f[key].value === 'object') {
          this.queryParams[key] = this.f[key].value.identifier;
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
      if (params[key].includes('HP:') || params[key].includes('GO:')) {
        this.phenotypeNeigborhood = null;
        this.phenotypeLoading = false
      }
      delete params[key];
    }
    this.queryParams = params;
    this.navigate();
  }

  clearFilters() {
    this.queryParams = {};
    this.searchedTermsObjs = [];
    this.phenotypeNeigborhood = null;
    this.phenotypeLoading = false
    this.navigate();
  }

  setFormValues(){
    let formVal = {
      Consequence: [],
      ClinSig: [],
      'SIFT_object.term': [],
      'PolyPhen_object.term': [],
      AFMin: '',
      AFMax: '',
      'ontology_filter' : null 
    };
    Object.keys(this.queryParams).forEach(val => {
      // console.log(val, this.queryParams[val])
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
      } else {
        formObj[key] = value;
      }
    }
    // console.log(key, value, formObj);
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
    this.initPhenotypeFilter();
    this.findVariantRecords();
    this.setSearchLabels();
  }

  keys = Object.keys;

  trackByFn(item: any) {
    return item.class;
  }

  loadPhenotype() {
    this.phenotype$ = concat(
        of([]), // default items
        this.phenotypeInput$.pipe(
            distinctUntilChanged(),
            tap(() => this.phenotypeLoading = true),
            switchMap(term => this.lookupSrv.findEntityByLabelStartsWith(term, ['HP', 'GO'], 10).pipe(
                catchError(() => of([])), // empty list on error
                tap(() => this.phenotypeLoading = false)
            ))
        )
    );
  }

  initPhenotypeFilter(){
    if (this.queryParams['ontology_filter']) {
      let phenotype = this.queryParams['ontology_filter'];
      if(this.phenotypeNeigborhood) {
        console.log(this.phenotypeNeigborhood.class, this.phenotypeNeigborhood.class.class == this.queryParams['ontology_filter'].replace(':', '_'));
      }
      if (!this.phenotypeNeigborhood || (this.phenotypeNeigborhood && this.phenotypeNeigborhood.class.class.split('/').pop() != phenotype.replace(':', '_'))) {
        phenotype = 'http://purl.obolibrary.org/obo/' + phenotype.replace(':', '_');
        this.getPhenotypeNeigborhood(phenotype);
      }
    }
  }

  getPhenotypeNeigborhood(phenotype) {
    this.phenotypeNeigborhood = {};
    this.lookupSrv.findEquivalent(phenotype, 'HP').subscribe(res => {
      this.phenotypeNeigborhood['class'] = res ? res['result'][0] : null;
    });

    this.lookupSrv.findSuperClass(phenotype, 'HP').subscribe(res => {
      this.phenotypeNeigborhood['superclass'] = res && res['result'].length > 0 ? res['result'][0]: null;
    });

    this.lookupSrv.findSubClass(phenotype, 'HP').subscribe(res => {
      this.phenotypeNeigborhood['subclass'] = res && res['result'].length > 0 ? res['result'] : [];
    });
  }

  resolveOntologyClasses(goClasses, phenotypeClasses){
    if (goClasses.length > 0) {
      this.lookupSrv.findEntityByOboId(goClasses).subscribe(data => {
        data.forEach(element => {
          this.goCache[element.identifier] = element;
        });
      });
    }

    if (phenotypeClasses.length > 0) {
      this.lookupSrv.findEntityByOboId(phenotypeClasses).subscribe(data => {
        data.forEach(element => {
          this.hpCache[element.identifier] = element;
        });
      });
    }
  }


  exportRecords() {
    let filter = Object.assign({}, this.queryParams);
    let params = new URLSearchParams();
    for(let key in filter){
        params.set(key, filter[key]) 
    }

    window.open(`/api/job/${this.jobId}/record/_export?${params.toString()}`);
  }

}
