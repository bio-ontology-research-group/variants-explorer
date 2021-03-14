import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { VariantsExplorerService } from '../variants-explorer.service';

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

  constructor(private veSrv: VariantsExplorerService,
    private route: ActivatedRoute) { 
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

    this.veSrv.findRecords(this.jobId, this.pageSize, offset).subscribe(res => {
      this.variantRecords = res['data'] && res['data'].length > 1 ? res['data'] : []; 
      this.collectionSize = res['total'];
    });

  }

}
