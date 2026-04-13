import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { environment } from '../../../../Core/Environments/environment';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class TestSer {
   private http=inject(HttpClient);
 private readonly PREVIEW_BASE_URL = environment.PREVIEW_BASE_URL;
 private readonly REQUEST_TIMEOUT = 30000; // 30 seconds
  private readonly NAV_STATE_KEY = 'testNavigationState';
  private readonly RESULT_KEY = 'testResultData';


 getTestDetails( testId: string, q_id: number, emp_code: string): Observable<any> {
    const payload = {
      test_id: parseInt(testId),
      q_id: q_id,
      emp_code: emp_code
    };

    console.log('Service calling API with payload:', payload);

    return this.http.post<any>(`${this.PREVIEW_BASE_URL}/questions/start-test`,payload);
  }


// submitTestAnswers(t_id: number, emp_id: string, responses: any): Observable<any> {
//     const payload = {
//       t_id: t_id,
//       emp_id: emp_id,
//       responses: responses
//     };

//     console.log('Service submitting answers with payload:', payload);

//     return this.http.post<any>(
//       `${this.PREVIEW_BASE_URL}/submit-answer/`,
//       payload
//     );
//   }



// submitTestAnswers(t_id: number, emp_id: number, responses: any): Observable<any> {
//   // ✅ emp_id is now a number, not string
//   const payload = {
//     t_id: t_id,
//     emp_id: emp_id,  // Send as number, not string
//     responses: responses
//   };

//   console.log('Service submitting answers with payload:', payload);
//   console.log('emp_id type:', typeof emp_id, 'value:', emp_id);

//   return this.http.post<any>(
//     `${this.PREVIEW_BASE_URL}/submit-answer/`,
//     payload
//   );
// }


submitTestAnswers(t_id: number, emp_id: number | string, responses: any): Observable<any> {
  // ✅ Convert emp_id to number if it's a string
  const numericEmpId = typeof emp_id === 'string' ? parseInt(emp_id, 10) : emp_id;
  
  const payload = {
    t_id: t_id,
    emp_id: numericEmpId,  // Send as number
    responses: responses
  };

  console.log('Service submitting answers with payload:', payload);
  console.log('emp_id type:', typeof numericEmpId, 'value:', numericEmpId);

  return this.http.post<any>(
    `${this.PREVIEW_BASE_URL}/submit-answer/`,
    payload
  );
}





  storeTestResult(resultData: any): void {
    if (!resultData) {
      console.warn('⚠️ Attempting to store null/undefined result');
      return;
    }

    try {
      sessionStorage.setItem(this.RESULT_KEY, JSON.stringify(resultData));
      console.log('✅ Test result stored:', resultData);
    } catch (error) {
      console.error('❌ Error storing test result:', error);
    }
  }

  /**
   * ✅ NEW: Retrieve test result
   */
  getTestResult(): any {
    try {
      const result = sessionStorage.getItem(this.RESULT_KEY);
      if (result) {
        console.log('✅ Test result retrieved');
        return JSON.parse(result);
      }
      console.warn('⚠️ No test result found');
      return null;
    } catch (error) {
      console.error('❌ Error retrieving test result:', error);
      return null;
    }
  }

  /**
   * ✅ NEW: Clear test result
   */
  clearTestResult(): void {
    try {
      sessionStorage.removeItem(this.RESULT_KEY);
      console.log('✅ Test result cleared');
    } catch (error) {
      console.error('❌ Error clearing test result:', error);
    }
  }

  /**
   * Store navigation state in session storage
   */
  storeNavigationState(state: any): void {
    if (!state) {
      console.warn('⚠️ Attempting to store null/undefined state');
      return;
    }

    try {
      sessionStorage.setItem(this.NAV_STATE_KEY, JSON.stringify(state));
      console.log('✅ Navigation state stored:', state);
    } catch (error) {
      console.error('❌ Error storing navigation state:', error);
    }
  }

  /**
   * Retrieve navigation state from session storage
   */
  getNavigationState(): any {
    try {
      const state = sessionStorage.getItem(this.NAV_STATE_KEY);
      if (state) {
        console.log('✅ Navigation state retrieved');
        return JSON.parse(state);
      }
      console.warn('⚠️ No navigation state found');
      return null;
    } catch (error) {
      console.error('❌ Error retrieving navigation state:', error);
      return null;
    }
  }

  /**
   * Clear navigation state from session storage
   */
  clearNavigationState(): void {
    try {
      sessionStorage.removeItem(this.NAV_STATE_KEY);
      console.log('✅ Navigation state cleared');
    } catch (error) {
      console.error('❌ Error clearing navigation state:', error);
    }
  }

  /**
   * Check if navigation state exists
   */
  hasNavigationState(): boolean {
    return sessionStorage.getItem(this.NAV_STATE_KEY) !== null;
  }

  /**
   * Validate test parameters
   */
  validateTestParams(testId: any, empCode: any, qId: any): boolean {
    const isValid = testId && empCode && (qId || qId === 0);
    
    if (!isValid) {
      console.warn('⚠️ Invalid test parameters:', {
        testId: testId || 'MISSING',
        empCode: empCode || 'MISSING',
        qId: qId !== undefined ? qId : 'MISSING'
      });
    }

    return isValid;
  }
}

