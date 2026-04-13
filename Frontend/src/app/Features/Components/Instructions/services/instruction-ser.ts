import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment } from '../../../../Core/Environments/environment';
import { Observable } from 'rxjs';
import { InstructionsResponse } from '../../../../Shared/Interfaces/instructionsresponse';

@Injectable({
  providedIn: 'root',
})
export class InstructionSer {
  private http=inject(HttpClient);
 private readonly PREVIEW_BASE_URL = environment.PREVIEW_BASE_URL;

  getInstructions(testId: string, emp_code: string, full_name: string): Observable<InstructionsResponse>{
    // return this.http.get<any>(`https://api.example.com/instructions/${testId}`);
  // return this.http.post<any>(`${this.API_BASE_URL}/instructions/${testId}`);
   const body = {
      emp_code: emp_code,
      full_name: full_name
    };

    return this.http.post<InstructionsResponse>(
      `${this.PREVIEW_BASE_URL}/instructions/${testId}`,
      body
    );
  }







  private readonly INSTRUCTION_KEY = 'testInstructionData';

storeInstructionData(data: any): void {
  try {
    sessionStorage.setItem(this.INSTRUCTION_KEY, JSON.stringify(data));
    console.log('✅ Instruction data stored:', data);
  } catch (error) {
    console.error('❌ Error storing instruction data:', error);
  }
}

getInstructionData(): any {
  try {
    const data = sessionStorage.getItem(this.INSTRUCTION_KEY);
    if (data) {
      console.log('✅ Instruction data retrieved');
      return JSON.parse(data);
    }
    console.warn('⚠️ No instruction data found');
    return null;
  } catch (error) {
    console.error('❌ Error retrieving instruction data:', error);
    return null;
  }
}

clearInstructionData(): void {
  try {
    sessionStorage.removeItem(this.INSTRUCTION_KEY);
    console.log('✅ Instruction data cleared');
  } catch (error) {
    console.error('❌ Error clearing instruction data:', error);
  }
}
 
}
