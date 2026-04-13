import { MCQQuestion, TFQuestion, FillInTheBlankQuestion, ScenarioQuestion, QuestionsResponse, UserAnswersData,PersonData } from './../../../../../Shared/Interfaces/Testpage';
import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { interval, Subscription } from 'rxjs';
import { takeWhile } from 'rxjs/operators';
import { Navbar } from '../../../Navbar/pages/navbar/navbar';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { TestSer } from '../../services/test-ser';
import { UserNavbar } from '../../../userNavbar/pages/user-navbar/user-navbar';


@Component({
  selector: 'app-test-page',
  imports: [Navbar,CommonModule,UserNavbar],
  templateUrl: './test-page.html',
  styleUrl: './test-page.scss',
})


export class TestPage implements OnInit, OnDestroy {
  // Constants
  private readonly TEST_DURATION = 30 * 60; // 30 minutes
  durationInMinutes: number = 30;

  // State Variables
  questions: QuestionsResponse | null = null;
  userAnswers: { [key: number]: UserAnswersData } = {};
  currentPersonIndex: number = 0;
  timeLeft: number = this.TEST_DURATION;
  submitted: boolean = false;
  loading: boolean = true;
  error: boolean = false;
  errorMessage: string = '';
  TEST_ID: number = 0;
  EMP_CODE: string = '';
  EMP_ID: number = 0; 
  Q_ID: number = 0;
  // Display Properties
  unAttemptedCount: number = 0;
  attemptedCount: number = 0;
  timerDisplay: string = '00h30m00s';
  personIndices: number[] = [];
  optionNumbers: number[] = [1, 2, 3, 4];
  tfOptions: string[] = ['True', 'False'];
   isSubmitting: boolean = false;

  private timerSubscription: Subscription | null = null;

  constructor(private http: HttpClient,private cdr: ChangeDetectorRef,private router:Router,private testser:TestSer) {}

  ngOnInit(): void {
    this.initializeFromRouterState();
    if (this.TEST_ID && this.EMP_CODE) {
    this.fetchQuestions();
  }
  }

  ngOnDestroy(): void {
    this.stopTimer();
  }




private initializeFromRouterState(): void {
  const state = this.testser.getNavigationState();

  if (state) {
    this.TEST_ID = state['test_id'] || 0;
    this.EMP_CODE = state['emp_code'] || '';
    this.Q_ID = state['q_id'] || 0;

    console.log('Navigation State Data:', {
      test_id: this.TEST_ID,
      q_id: this.Q_ID,
      emp_code: this.EMP_CODE
    });

    this.testser.clearNavigationState();
  }

  if (!this.TEST_ID || !this.EMP_CODE || !this.Q_ID) {
    this.error = true;
    this.errorMessage = 'Missing required data. Please go back and start the test again.';
    this.loading = false;
    console.error('Missing required state data:', { TEST_ID: this.TEST_ID, EMP_CODE: this.EMP_CODE, Q_ID: this.Q_ID });
    this.cdr.markForCheck();
    return;
  }
}
  
 



// fetchQuestions(): void {
//   this.loading = true;
//   this.error = false;
//   this.cdr.markForCheck();

//   this.testser.getTestDetails(String(this.TEST_ID), this.Q_ID, this.EMP_CODE)
//     .subscribe({
//       next: (response) => {
//         try {
//           let parsedQuestions;
          
//           // Handle both formats
//           // if (response[0]?.question_text) {
//           //   parsedQuestions = JSON.parse(response[0].question_text);
//           // } else if (response.question_text) {
//           //   parsedQuestions = JSON.parse(response.question_text);
//           // } else {
//           //   parsedQuestions = response;
//           // }


//           // Handle array response format
//           const apiData = Array.isArray(response) ? response[0] : response;
          
//           // ✅ Check if question_text is a STRING or OBJECT
//           if (typeof apiData?.question_text === 'string') {
//             // If it's a string, parse it
//             parsedQuestions = JSON.parse(apiData.question_text);
//           } else if (typeof apiData?.question_text === 'object') {
//             // If it's already an object, use it directly
//             parsedQuestions = apiData.question_text;
//           } else {
//             throw new Error('question_text format not recognized');
//           }

//           this.questions = this.transformResponse(parsedQuestions, response);
//           this.setTestDuration(response);

//           this.initializeUserAnswers();
//           this.generatePersonIndices();
//           this.loading = false;
//           this.updateStats();
//           this.startTimer();
//           this.cdr.markForCheck();
//         } catch (error) {
//           this.handleParseError(error);
//         }
//       },
//       error: (err) => this.handleFetchError(err)
//     });
// }

 fetchQuestions(): void {
    this.loading = true;
    this.error = false;
    this.cdr.markForCheck();

    this.testser.getTestDetails(String(this.TEST_ID), this.Q_ID, this.EMP_CODE)
      .subscribe({
        next: (response) => {
          try {
            // ✅ Extract emp_id from API response
            const apiData = Array.isArray(response) ? response[0] : response;
            
            // Store the actual emp_id from API
            if (apiData?.emp_id) {
              this.EMP_ID = apiData.emp_id;
              console.log('✅ emp_id from API:', this.EMP_ID);
            }

            // Handle question_text
            let parsedQuestions;
            if (typeof apiData?.question_text === 'string') {
              parsedQuestions = JSON.parse(apiData.question_text);
            } else if (typeof apiData?.question_text === 'object') {
              parsedQuestions = apiData.question_text;
            } else {
              throw new Error('question_text format not recognized');
            }

            this.questions = this.transformResponse(parsedQuestions, response);
            this.setTestDuration(response);

            this.initializeUserAnswers();
            this.generatePersonIndices();
            this.loading = false;
            this.updateStats();
            this.startTimer();
            this.cdr.markForCheck();
          } catch (error) {
            this.handleParseError(error);
          }
        },
        error: (err) => this.handleFetchError(err)
      });
  }



private setTestDuration(response: any): void {
  let minutes = 30; // Default 30 minutes

  // Handle array response format
  if (response[0]?.duration) {
    minutes = response[0].duration;
  } 
  // Handle direct response format
  else if (response.duration) {
    minutes = response.duration;
  }

  // Store duration in minutes
  this.durationInMinutes = minutes;
  
  // Convert to seconds for countdown timer
  this.timeLeft = minutes * 60;
  this.timerDisplay = this.formatTime(this.timeLeft);
  
  console.log(`✅ Test Duration: ${minutes} minutes`);
  this.cdr.markForCheck();
}


private transformResponse(parsedQuestions: any, response: any): QuestionsResponse {
  return {
    test_id: response.test_id || response[0]?.test_id,
    q_id: response.q_id || response[0]?.q_id,
    emp_code: response.emp_code || response[0]?.emp_code,
    people: 1,
    'person 1': {
      // Map the actual API field names to your expected format
      mcq: parsedQuestions['all mcq questions'] || [],
      'true/false': parsedQuestions['all true/false questions'] || [],
      'fill in the blanks': parsedQuestions['all fill in the blanks questions'] || [],
      scenario: parsedQuestions['all scenario questions'] || []
    }
  } as QuestionsResponse;
}

private handleParseError(error: any): void {
  this.error = true;
  this.errorMessage = 'Failed to parse questions: Invalid JSON format';
  this.loading = false;
  this.cdr.markForCheck();
}

private handleFetchError(err: any): void {
  this.error = true;
  this.errorMessage = `Failed to load questions: ${err.message || 'Unknown error'}`;
  this.loading = false;
  this.cdr.markForCheck();
}



  /**
   * Initialize user answers object based on questions
   */
  private initializeUserAnswers(): void {
    if (!this.questions) return;

    this.userAnswers = {};
    for (let i = 0; i < this.questions.people; i++) {
      const person = this.questions[`person ${i + 1}`] as PersonData;
      this.userAnswers[i] = {
        mcq: person.mcq?.map(() => '') || [],
        'true/false': person['true/false']?.map(() => '') || [],
        'fill in the blanks': person['fill in the blanks']?.map(() => '') || [],
        scenario: person.scenario?.map(() => '') || []
      };
    }
  }

  /**
   * Generate array of person indices
   */
  private generatePersonIndices(): void {
    if (!this.questions) {
      this.personIndices = [];
      return;
    }
    this.personIndices = Array.from({ length: this.questions.people }, (_, i) => i);
  }

  /**
   * Get current person's data
   */
  get currentPersonData(): PersonData | null {
    if (!this.questions) return null;
    const data = this.questions[`person ${this.currentPersonIndex + 1}`];
    return data as PersonData || null;
  }

  /**
   * Get option value from question safely
   */
  getOptionValue(question: any, optNum: number): string {
    return question[`option ${optNum}`] || '';
  }

  /**
   * Get current answer for a question
   */
  getCurrentAnswer(type: keyof UserAnswersData, index: number): string {
    return this.userAnswers[this.currentPersonIndex]?.[type]?.[index] || '';
  }

  /**
   * Set answer for a question
   */
  setAnswer(type: keyof UserAnswersData, index: number, value: string): void {
    if (!this.userAnswers[this.currentPersonIndex]) {
      this.userAnswers[this.currentPersonIndex] = {
        mcq: [],
        'true/false': [],
        'fill in the blanks': [],
        scenario: []
      };
    }
    this.userAnswers[this.currentPersonIndex][type][index] = value;
    this.updateStats();
    this.cdr.markForCheck();
  }

  /**
   * Update statistics
   */
  private updateStats(): void {
    this.unAttemptedCount = this.getUnAttemptedCount();
    this.attemptedCount = this.getAttemptedCount();
    this.cdr.markForCheck();
  }

  /**
   * Get unattempted questions count
   */
  private getUnAttemptedCount(): number {
    if (!this.currentPersonData) return 0;

    const currentAnswers = this.userAnswers[this.currentPersonIndex];
    if (!currentAnswers) return 0;

    let unattempted = 0;

    // Count empty MCQ answers
    currentAnswers.mcq.forEach((ans) => {
      if (!ans || ans.trim() === '') unattempted++;
    });

    // Count empty True/False answers
    currentAnswers['true/false'].forEach((ans) => {
      if (!ans || ans.trim() === '') unattempted++;
    });

    // Count empty Fill in the Blanks answers
    currentAnswers['fill in the blanks'].forEach((ans) => {
      if (!ans || ans.trim() === '') unattempted++;
    });

    // Count empty Scenario answers
    currentAnswers.scenario.forEach((ans) => {
      if (!ans || ans.trim() === '') unattempted++;
    });

    return unattempted;
  }

  /**
   * Get attempted questions count
   */
  private getAttemptedCount(): number {
    if (!this.currentPersonData) return 0;

    const totalQuestions =
      (this.currentPersonData.mcq?.length || 0) +
      (this.currentPersonData['true/false']?.length || 0) +
      (this.currentPersonData['fill in the blanks']?.length || 0) +
      (this.currentPersonData.scenario?.length || 0);

    return totalQuestions - this.getUnAttemptedCount();
  }

  /**
   * Start the timer
   */
  private startTimer(): void {
    if (this.timerSubscription) {
      this.timerSubscription.unsubscribe();
    }

    this.timerSubscription = interval(1000)
      .pipe(takeWhile(() => this.timeLeft > 0))
      .subscribe(() => {
        this.timeLeft--;
        this.timerDisplay = this.formatTime(this.timeLeft);
        this.cdr.markForCheck();

        if (this.timeLeft <= 0) {
          this.stopTimer();
          this.submitTest();
        }
      });
  }

  /**
   * Stop the timer
   */
  private stopTimer(): void {
    if (this.timerSubscription) {
      this.timerSubscription.unsubscribe();
      this.timerSubscription = null;
    }
  }

   


































private showSuccessMessage(): void {
  console.log('Test submitted successfully!');
  // Optional: Navigate to results page or show success modal
  // this.router.navigate(['/test-results']);
}





private getNumericEmpId(): number {
  // Extract digits from emp_code (e.g., "ntz5469" -> 5469)
  const match = this.EMP_CODE.match(/\d+/);
  if (match) {
    return parseInt(match[0], 10);
  }
  return 0; // Fallback
}

// 2. Update buildResponsePayload to match backend structure
private buildResponsePayload(): any {
  const currentAnswers = this.userAnswers[this.currentPersonIndex];
  const currentQuestions = this.currentPersonData;

  if (!currentAnswers || !currentQuestions) {
    console.warn('No answers or questions found');
    return null;
  }

  // Build structure matching backend expectations
  const personData: any = {
    mcq: [],
    scenario: [],
    'true/false': [],
    'fill in the blanks': []
  };

  // Process MCQ questions
  if (currentQuestions.mcq && currentAnswers.mcq) {
    personData.mcq = currentQuestions.mcq.map((question: any, index: number) => ({
      question: question.question || '',
      option_1: question['option 1'] || '',
      option_2: question['option 2'] || '',
      option_3: question['option 3'] || '',
      option_4: question['option 4'] || '',
      answer: question.answer || '',
      user_answer: currentAnswers.mcq[index] || null
    }));
  }

  // Process Scenario questions
  if (currentQuestions.scenario && currentAnswers.scenario) {
    personData.scenario = currentQuestions.scenario.map((question: any, index: number) => ({
      question: question.question || '',
      user_answer: currentAnswers.scenario[index] || null
    }));
  }

  // Process True/False questions
  if (currentQuestions['true/false'] && currentAnswers['true/false']) {
    personData['true/false'] = currentQuestions['true/false'].map((question: any, index: number) => ({
      question: question.question || '',
      option_1: 'True',
      option_2: 'False',
      answer: question.answer || '',
      user_answer: currentAnswers['true/false'][index] || null
    }));
  }

  // Process Fill in the Blanks questions
  if (currentQuestions['fill in the blanks'] && currentAnswers['fill in the blanks']) {
    personData['fill in the blanks'] = currentQuestions['fill in the blanks'].map((question: any, index: number) => ({
      question: question.question || '',
      answer: question.answer || '',
      user_answer: currentAnswers['fill in the blanks'][index] || null
    }));
  }

  // Return structure matching backend
  return {
    people: 1,
    'person 1': personData
  };
}



// submitTest(): void {
//     if (this.submitted) return;

//     try {
//       const responsePayload = this.buildResponsePayload();

//       if (!responsePayload) {
//         this.error = true;
//         this.errorMessage = 'No answers to submit';
//         this.cdr.markForCheck();
//         return;
//       }

//       // ✅ Use the emp_id stored from API response
//       if (!this.EMP_ID || this.EMP_ID === 0) {
//         this.error = true;
//         this.errorMessage = 'Invalid employee ID. Please start the test again.';
//         this.cdr.markForCheck();
//         return;
//       }

//       console.log('Submitting with TEST_ID:', this.TEST_ID, 'EMP_ID:', this.EMP_ID);
//       console.log('Response payload:', responsePayload);

//       // Pass the stored EMP_ID
//       this.testser.submitTestAnswers(this.TEST_ID, this.EMP_ID, responsePayload)
//         .subscribe({
//           next: (response) => {
//             console.log('Submit success:', response);
//             this.submitted = true;
//             this.stopTimer();
//             this.navigateToResults(response);
//             this.cdr.markForCheck();
//           },
//           error: (err) => this.handleSubmitError(err)
//         });
//     } catch (error: any) {
//       this.error = true;
//       this.errorMessage = `Error: ${error.message}`;
//       this.cdr.markForCheck();
//     }
//   }

 submitTest(): void {
    if (this.submitted) return;

    try {
      const responsePayload = this.buildResponsePayload();

      if (!responsePayload) {
        this.error = true;
        this.errorMessage = 'No answers to submit';
        this.cdr.markForCheck();
        return;
      }

      if (!this.EMP_ID || this.EMP_ID === 0) {
        this.error = true;
        this.errorMessage = 'Invalid employee ID. Please start the test again.';
        this.cdr.markForCheck();
        return;
      }

      // ✅ Set isSubmitting to true to show loader
      this.isSubmitting = true;
      this.cdr.markForCheck();

      console.log('Submitting with TEST_ID:', this.TEST_ID, 'EMP_ID:', this.EMP_ID);
      console.log('Response payload:', responsePayload);

      this.testser.submitTestAnswers(this.TEST_ID, this.EMP_ID, responsePayload)
        .subscribe({
          next: (response) => {
            console.log('Submit success:', response);
            this.submitted = true;
            this.stopTimer();
            this.navigateToResults(response);
            // ✅ Set isSubmitting to false when done
            this.isSubmitting = false;
            this.cdr.markForCheck();
          },
          error: (err) => {
            this.handleSubmitError(err);
            // ✅ Set isSubmitting to false on error
            this.isSubmitting = false;
            this.cdr.markForCheck();
          }
        });
    } catch (error: any) {
      this.error = true;
      this.errorMessage = `Error: ${error.message}`;
      // ✅ Set isSubmitting to false on error
      this.isSubmitting = false;
      this.cdr.markForCheck();
    }
  }


private handleSubmitError(err: any): void {
  console.error('Submit error:', err);
  this.error = true;
  this.errorMessage = `Failed to submit: ${err.error?.message || err.message || 'Unknown error'}`;
  this.cdr.markForCheck();
}



 private navigateToResults(apiResponse: any): void {
    this.testser.storeTestResult({
      test_id: this.TEST_ID,
      emp_code: this.EMP_CODE,
      emp_id: this.EMP_ID,  // ✅ Store the correct emp_id
      submitted_at: new Date(),
      result: apiResponse
    });

    this.router.navigate(['/test-results']);
  }



  /**
   * Switch to another person's questions
   */
  switchPerson(index: number): void {
    this.currentPersonIndex = index;
    this.updateStats();
    window.scrollTo({ top: 0, behavior: 'smooth' });
    this.cdr.markForCheck();
  }

  /**
   * Format time for display
   */
  private formatTime(seconds: number): string {
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}h${mins.toString().padStart(2, '0')}m${secs.toString().padStart(2, '0')}s`;
  }





get allQuestionsAnswered(): boolean {
  if (!this.currentPersonData) return false;

  const currentAnswers = this.userAnswers[this.currentPersonIndex];
  if (!currentAnswers) return false;

  // Check MCQ answers
  if (this.currentPersonData.mcq && this.currentPersonData.mcq.length > 0) {
    const unansweredMcq = currentAnswers.mcq.some(ans => !ans || ans.trim() === '');
    if (unansweredMcq) return false;
  }

  // Check True/False answers
  if (this.currentPersonData['true/false'] && this.currentPersonData['true/false'].length > 0) {
    const unansweredTF = currentAnswers['true/false'].some(ans => !ans || ans.trim() === '');
    if (unansweredTF) return false;
  }

  // Check Fill in the Blanks answers
  if (this.currentPersonData['fill in the blanks'] && this.currentPersonData['fill in the blanks'].length > 0) {
    const unansweredFIB = currentAnswers['fill in the blanks'].some(ans => !ans || ans.trim() === '');
    if (unansweredFIB) return false;
  }

  // Check Scenario answers
  if (this.currentPersonData.scenario && this.currentPersonData.scenario.length > 0) {
    const unansweredScenario = currentAnswers.scenario.some(ans => !ans || ans.trim() === '');
    if (unansweredScenario) return false;
  }

  // All questions are answered
  return true;
}

/**
 * Get total number of questions
 */
get totalQuestions(): number {
  if (!this.currentPersonData) return 0;

  return (
    (this.currentPersonData.mcq?.length || 0) +
    (this.currentPersonData['true/false']?.length || 0) +
    (this.currentPersonData['fill in the blanks']?.length || 0) +
    (this.currentPersonData.scenario?.length || 0)
  );
}

/**
 * Get message for submit button based on state
 */
get submitButtonMessage(): string {
  if (this.allQuestionsAnswered) {
    return 'Submit';
  }
  return `Complete all ${this.unAttemptedCount} unanswered question(s)`;
}




}