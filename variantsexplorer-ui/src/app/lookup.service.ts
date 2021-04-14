import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { of } from 'rxjs';

@Injectable()
export class LookupService {

  PHENOME_API_URI = 'http://phenomebrowser.net/api'
  ABEROWL_API_URI = 'http://aber-owl.net/api'

  options = {
    headers:  new HttpHeaders({
      'Accept': 'application/json'
    })
  };

  constructor(private http: HttpClient) { 
  }

  findEntityByLabelStartsWith(term: string, valueset: string[], pagesize:number) {
    if (term === '' || valueset.length < 1) {
      return of([]);
    }

    var queryStr = `term=${term}`;
    valueset.forEach(function (value) {
      queryStr += "&valueset=" + value;
    });
    if (pagesize) {
      queryStr += "&pagesize=" + pagesize;
    }
    return this.http.get(`${this.PHENOME_API_URI}/entity/_startswith?${queryStr}`, this.options);
  }

  findEntityByIris(iris:any[], valueset:string) {
    var req;
    if (!valueset) {
      req = {'iri': iris}
    } else {
      req = {'iri': iris, valueset: valueset}
    }
    return this.http.post(`${this.PHENOME_API_URI}/entity/_findbyiri`, req, this.options);
  }

  findSuperClass(classIdentifier: string, ontology:string) {
    return this.executeDlQuery(classIdentifier, 'superclass', ontology);
  }

  findSubClass(classIdentifier: string, ontology:string) {
    return this.executeDlQuery(classIdentifier, 'subclass', ontology);
  }

  findEquivalent(classIdentifier: string, ontology:string) {
    return this.executeDlQuery(classIdentifier, 'equivalent', ontology);
  }
  executeDlQuery(classIdentifier: string, type: string, ontology:string) {
    let params = new URLSearchParams();
    params.set('query', classIdentifier); 
    params.set('type', type); 
    params.set('ontology', ontology); 

    return this.http.get(`/api/aberowl/dlquery?${params.toString()}`, this.options);
  }

}
