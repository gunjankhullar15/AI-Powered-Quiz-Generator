import { inject, Injectable } from '@angular/core';
import { environment } from '../../../../Core/Environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs/internal/Observable';

@Injectable({
  providedIn: 'root',
})
export class CandidateinfoSer {
   private readonly PREVIEW_BASE_URL = environment.PREVIEW_BASE_URL;
   testId: string = '';

  private http=inject(HttpClient);

  loadInfo(testId:string) :Observable<any> {

   return  this.http.get<any>(`${this.PREVIEW_BASE_URL}/employees/get-candidates/${testId}`);

  }



//   loadInfo(testId: string): Observable<any> {
//    const url = `${this.API_BASE_URL}/employees/get-candidates/${testId}`;
//    console.log('Service making request to:', url);  // Debug log
//    return this.http.get<any>(url);
// }
}
