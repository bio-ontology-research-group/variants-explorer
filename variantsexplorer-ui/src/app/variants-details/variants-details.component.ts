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
  constructor(private veSrv: VariantsExplorerService,
    private route: ActivatedRoute) { 
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.veSrv.getJob(params.id).subscribe(res => {
        this.job = res
        console.log(this.job, this.job['entries'])
      });
    });
  }

}
