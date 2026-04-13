import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment } from '../../../../Core/Environments/environment';
import { Observable } from 'rxjs';
@Injectable({
  providedIn: 'root',
})
export class TesthistorySer {
  private readonly PREVIEW_BASE_URL = environment.PREVIEW_BASE_URL;

  private HttpClient=inject(HttpClient);

  getAllTests():Observable<any> {

   return  this.HttpClient.get<any>(`${this.PREVIEW_BASE_URL}/tests/get-all-tests`);

    
  }
}
