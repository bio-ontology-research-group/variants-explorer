import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { _ } from 'underscore';
import { Observable } from 'rxjs';

@Injectable()
export class VariantsExplorerService {
  URL="api/job"
  options = {
    headers:  new HttpHeaders({
      'Accept': 'application/json'
    })
  };

  constructor(private http: HttpClient) { }



  // find(disease: string, rankType:string): Observable<any> {
  //   var query_string = 'disease=' + disease;
  //   if (rankType) {
  //     query_string += 'ranktype=' + rankType;
  //   }

  //   return this.http.get(`/api/cohort?${query_string}`, this.options);
  // }

  find(): Observable<any>  {
    var url = `${this.URL}`;
    return this.http.get(url, this.options);
  }


  getJob(id): Observable<any>  {
    var url = `${this.URL}/${id}`;
    return this.http.get(url, this.options);
  }

  deleteJob(id): Observable<any>  {
    var url = `${this.URL}/${id}`;
    return this.http.delete(url, this.options);
  }
  
  
  submitJob(formData){
    return this.http.post<any>(`${this.URL}`, formData, {  
       reportProgress: true,  
       observe: 'events'  
    });  
  }

}
