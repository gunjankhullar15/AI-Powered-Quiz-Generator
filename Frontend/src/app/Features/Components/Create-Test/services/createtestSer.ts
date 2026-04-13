import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment } from '../../../../Core/Environments/environment';

@Injectable({
  providedIn: 'root',
})
export class CreatetestSer {
  // private readonly API_BASE_URL = environment.API_BASE_URL;
  private readonly PREVIEW_BASE_URL = environment.PREVIEW_BASE_URL;

private http=inject(HttpClient);

  getweightage(){
    return this.http.get<any>(`${this.PREVIEW_BASE_URL}/weightages/get-weightages`);
  }

  deleteTest(){
    return this.http.delete<any>(`${this.PREVIEW_BASE_URL}/clear-weaviate/`);
  }

onsubmitdoc(files: File | File[]) {
  const formData = new FormData();
  
  if (Array.isArray(files)) {
    // Multiple files - append each without the filename parameter
    files.forEach(file => {
      formData.append('files', file);
    });
  } else {
    // Single file - append without the filename parameter
    formData.append('files', files);
  }
  
  // Debug log
  console.log('FormData being sent:');
  for (let pair of formData.entries()) {
    console.log(pair[0], pair[1]);
  }
  
  return this.http.post<any>(`${this.PREVIEW_BASE_URL}/list-preview/`, formData);
}



  onsubmitarticle(url: string) {
    return this.http.get<any>(`${this.PREVIEW_BASE_URL}/article-preview/`, {
      params: {
        url: url
      }
    });
  }

  oncreatetest(data:any){
    return this.http.post<any>(`${this.PREVIEW_BASE_URL}/tests/create-test`,data);
  }

}
