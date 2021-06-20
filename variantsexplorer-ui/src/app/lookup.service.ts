import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';

@Injectable()
export class LookupService {

  PHENOME_API_URI = 'http://phenomebrowser.net/api'
  ABEROWL_API_URI = 'http://aber-owl.net/api'
  OBO_PREFIX = 'http://purl.obolibrary.org/obo/'
  UNIPROT_PREFIX = 'http://uniprot.org/uniprot/'


  P = 'http://phenomebrowser.net/api'

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

  findEntityByOboId(oboIds:any[]) : Observable<any> {
    let valueset = oboIds[0].split(':')[0];
    let iris = []
    let that = this
    oboIds.forEach(function (value) {
      iris.push(that.OBO_PREFIX + value.replace(':', '_')) 
    });

    var req = {iri: iris, valueset: valueset}  
    return this.http.post(`${this.PHENOME_API_URI}/entity/_findbyiri`, req, this.options);
  }

  findProtein(proteinIds:any[]) : Observable<any> {
    let valueset = 'Uniprot'
    let iris = []
    let that = this
    proteinIds.forEach(function (value) {
      iris.push(that.UNIPROT_PREFIX + value);
    });

    var req = {iri: iris, valueset: valueset}  
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
