import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserNavbar } from '../../../userNavbar/pages/user-navbar/user-navbar';
import { TestPage1Ser } from '../../../TestPage1/services/test-page1-ser';



@Component({
  selector: 'app-result',
  imports: [CommonModule,UserNavbar],
  templateUrl: './result.html',
  styleUrls: ['./result.scss'],
})


export class Result implements OnInit {
  testResult = {
    fullName: 'N/A',
    empCode: 'N/A',
    score: 0,
    totalMarks: 0,
    percentage: '0%',
    status: 'Pending',
    attempts: 1,
    testName: 'N/A'
  };

  isPassed: boolean = false;
  isFailed: boolean = false;
  loading: boolean = true;
  error: boolean = false;
  errorMessage: string = '';
  passingScore: number = 50;

  constructor(
    private testser: TestPage1Ser,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadTestResult();
  }

  /**
   * Load test result from service
   */
  private loadTestResult(): void {
    this.loading = true;
    this.error = false;

    try {
      // Get result from service
      const storedResult = this.testser.getTestResult();

      if (!storedResult) {
        this.error = true;
        this.errorMessage = 'No test result found. Please complete a test first.';
        this.loading = false;
        return;
      }

      console.log('📊 Result data retrieved:', storedResult);

      // Map stored data to testResult object
      this.mapResultData(storedResult);

      // Calculate pass/fail status
      this.determineStatus();

      this.loading = false;
    } catch (error: any) {
      console.error('❌ Error loading result:', error);
      this.error = true;
      this.errorMessage = `Error loading result: ${error.message}`;
      this.loading = false;
    }
  }

  /**
   * Map API response to testResult object
   */
  private mapResultData(storedResult: any): void {
    // Get the API response
    const apiResponse = storedResult.result || storedResult;

    console.log('API Response:', apiResponse);

    // ✅ Map the new API response format
    this.testResult.fullName = apiResponse.full_name || 'N/A';
    this.testResult.empCode = apiResponse.emp_code || 'N/A';
    this.testResult.score = apiResponse.score || 0;
    this.testResult.totalMarks = apiResponse.total_marks || 0;
    this.testResult.percentage = apiResponse.percentage || '0%';
    this.testResult.status = apiResponse.status || 'Pending';
    this.testResult.attempts = apiResponse.attempted || 1;
    this.testResult.testName = apiResponse.test_name || 'N/A';

    console.log('✅ Result data mapped:', this.testResult);
  }

  /**
   * Determine if test is passed or failed
   */
  private determineStatus(): void {
    // Extract numeric percentage value
    const percentageValue = parseFloat(this.testResult.percentage);

    if (percentageValue >= this.passingScore) {
      this.isPassed = true;
      this.isFailed = false;
    } else {
      this.isPassed = false;
      this.isFailed = true;
    }

    console.log('Status determined - Passed:', this.isPassed, 'Failed:', this.isFailed);
  }

  /**
   * Start test again
   */
  startTestAgain(): void {
    console.log('Starting test again...');
    
    // Clear result data
    this.testser.clearTestResult();
    
    // Navigate back to home or instructions
    this.router.navigate(['/inst/1']);
  }
}