import { MCQQuestion, TFQuestion, FillInTheBlankQuestion, ScenarioQuestion, QuestionsResponse, UserAnswersData, PersonData } from './../../../../../Shared/Interfaces/Testpage';
import { Component, OnInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { interval, Subscription } from 'rxjs';
import { takeWhile } from 'rxjs/operators';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { UserNavbar } from '../../../userNavbar/pages/user-navbar/user-navbar';
import { TestPage1Ser } from '../../services/test-page1-ser';
import { InstructionSer } from '../../../Instructions/services/instruction-ser';
import { MaterialModule } from '../../../../../Shared/Modules/materialModule';

interface QuestionNavItem {
  index: number;
  type: 'mcq' | 'true/false' | 'fill in the blanks' | 'scenario';
  questionIndex: number;
  isAnswered: boolean;
}

@Component({
  selector: 'app-test-page1',
  imports: [CommonModule, UserNavbar,MaterialModule],
  templateUrl: './test-page1.html',
  styleUrl: './test-page1.scss',
})







export class TestPage1 implements OnInit, OnDestroy {
  // Constants
  private readonly TEST_DURATION = 30 * 60; // 30 minutes
  durationInMinutes: number = 30;
  testTitle: string = 'Test';
  // State Variables
  questions: QuestionsResponse | null = null;
  userAnswers: { [key: number]: UserAnswersData } = {};
  currentPersonIndex: number = 0;
  currentQuestionIndex: number = 0; // NEW: Track current question being displayed
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
  
  // NEW: Question navigation
  questionNavigation: QuestionNavItem[] = [];
  currentQuestion: any = null;


// Subscriptions and handlers
  private timerSubscription: Subscription | null = null;
  private visibilityChangeHandler: any;
  private blurHandler: any;
  private devToolsCheckInterval: any;




  constructor(
    private http: HttpClient,
    private cdr: ChangeDetectorRef,
    private router: Router,
    private testser: TestPage1Ser,
    private instSer: InstructionSer 
  ) {}

 ngOnInit(): void {
    this.initializeFromRouterState();
    if (this.TEST_ID && this.EMP_CODE) {
      this.fetchQuestions();
    }
    // Enter fullscreen and prevent escape
    setTimeout(() => {
      this.enterFullScreen();
      this.preventEscapeKey();
      this.detectWindowSwitch();
      this.detectDevTools();
    }, 100);
  }

  ngOnDestroy(): void {
    this.stopTimer();
    this.exitFullScreen();
    this.removeEscapeKeyListener();
    this.removeWindowSwitchListeners();
    this.stopDevToolsDetection();
  }

 
private preventEscapeKey(): void {
    // Capture ESC key at the earliest phase
    document.addEventListener('keydown', this.handleKeyDown, true); // Use capture phase
    
    // Monitor fullscreen changes and re-enter immediately
    document.addEventListener('fullscreenchange', this.handleFullscreenChange);
    document.addEventListener('mozfullscreenchange', this.handleFullscreenChange);
    document.addEventListener('webkitfullscreenchange', this.handleFullscreenChange);
    document.addEventListener('msfullscreenchange', this.handleFullscreenChange);
  }


  private handleKeyDown = (event: KeyboardEvent): boolean|void => {
    if (event.key === 'Escape' || event.key === 'Esc') {
      event.preventDefault();
      event.stopPropagation();
      event.stopImmediatePropagation();
      
      // Auto-submit the test when ESC is pressed
      if (!this.submitted && !this.isSubmitting) {
        console.log('ESC pressed - Auto-submitting test');
        this.submitTest();
      }
      return false;
    }
  }





   private handleFullscreenChange = (): void => {
    // If user exits fullscreen during test, auto-submit
    if (!document.fullscreenElement && !this.submitted && !this.loading && !this.isSubmitting) {
      console.log('Fullscreen exited - Auto-submitting test');
      this.submitTest();
    }
  }


 private removeEscapeKeyListener(): void {
    document.removeEventListener('keydown', this.handleKeyDown, true);
    document.removeEventListener('fullscreenchange', this.handleFullscreenChange);
    document.removeEventListener('mozfullscreenchange', this.handleFullscreenChange);
    document.removeEventListener('webkitfullscreenchange', this.handleFullscreenChange);
    document.removeEventListener('msfullscreenchange', this.handleFullscreenChange);
  }



 
private detectWindowSwitch(): void {
    // Detect when user switches tabs or windows
    this.visibilityChangeHandler = () => {
      if (document.hidden && !this.submitted && !this.isSubmitting && !this.loading) {
        console.log('Window switched - Auto-submitting test');
        this.submitTest();
      }
    };

    // Detect window blur (clicking outside browser)
    this.blurHandler = () => {
      if (!this.submitted && !this.isSubmitting && !this.loading) {
        console.log('Window lost focus - Auto-submitting test');
        this.submitTest();
      }
    };

    document.addEventListener('visibilitychange', this.visibilityChangeHandler);
    window.addEventListener('blur', this.blurHandler);
  }


  private detectDevTools(): void {
    let devtoolsOpen = false;
    const threshold = 160; // DevTools detection threshold

    const checkDevTools = () => {
      if (!this.submitted && !this.isSubmitting && !this.loading) {
        const widthThreshold = window.outerWidth - window.innerWidth > threshold;
        const heightThreshold = window.outerHeight - window.innerHeight > threshold;
        
        // Check if console is opened via console timing
        const start = performance.now();
        debugger; // This will pause if DevTools is open
        const duration = performance.now() - start;

        if (widthThreshold || heightThreshold || duration > 100) {
          if (!devtoolsOpen) {
            devtoolsOpen = true;
            console.log('DevTools detected - Auto-submitting test');
            this.submitTest();
          }
        }
      }
    };

    // Check every 1 second
    this.devToolsCheckInterval = setInterval(checkDevTools, 1000);

    // Also detect right-click and common DevTools shortcuts
    document.addEventListener('contextmenu', (e) => {
      e.preventDefault();
      if (!this.submitted && !this.isSubmitting && !this.loading) {
        console.log('Right-click detected - Auto-submitting test');
        this.submitTest();
      }
    });

    // Detect F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C
    document.addEventListener('keydown', (e) => {
      if (
        e.key === 'F12' ||
        (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'J' || e.key === 'C')) ||
        (e.metaKey && e.altKey && (e.key === 'I' || e.key === 'J' || e.key === 'C'))
      ) {
        e.preventDefault();
        if (!this.submitted && !this.isSubmitting && !this.loading) {
          console.log('DevTools shortcut detected - Auto-submitting test');
          this.submitTest();
        }
      }
    });
  }

  // ✅ NEW: Remove window switch listeners
  private removeWindowSwitchListeners(): void {
    if (this.visibilityChangeHandler) {
      document.removeEventListener('visibilitychange', this.visibilityChangeHandler);
    }
    if (this.blurHandler) {
      window.removeEventListener('blur', this.blurHandler);
    }
  }

  // ✅ NEW: Stop DevTools detection
  private stopDevToolsDetection(): void {
    if (this.devToolsCheckInterval) {
      clearInterval(this.devToolsCheckInterval);
    }
  }








  private enterFullScreen(): void {
    const elem = document.documentElement;
    
    if (elem.requestFullscreen) {
      elem.requestFullscreen({ navigationUI: 'hide' } as any).catch(err => {
        console.log('Fullscreen requires user interaction.');
      });
    } else if ((elem as any).mozRequestFullScreen) {
      (elem as any).mozRequestFullScreen();
    } else if ((elem as any).webkitRequestFullscreen) {
      (elem as any).webkitRequestFullscreen();
    } else if ((elem as any).msRequestFullscreen) {
      (elem as any).msRequestFullscreen();
    }
  }


  private exitFullScreen(): void {
    if (document.fullscreenElement) {
      this.removeEscapeKeyListener();
      document.exitFullscreen().catch(err => {
        console.warn('Could not exit fullscreen mode:', err);
      });
    }
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

const instructionData = this.instSer.getInstructionData();
  if (instructionData) {
    this.testTitle = instructionData.title || 'Test';
    this.durationInMinutes = instructionData.duration || 30;
    // this.timeLeft = this.durationInMinutes * 60;
    console.log('✅ Loaded from instructions:', {
      title: this.testTitle,
      duration: this.durationInMinutes
    });
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

  fetchQuestions(): void {
    this.loading = true;
    this.error = false;
    this.cdr.markForCheck();

    this.testser.getTestDetails(String(this.TEST_ID), this.Q_ID, this.EMP_CODE)
      .subscribe({
        next: (response) => {
          try {
            const apiData = Array.isArray(response) ? response[0] : response;

            if (apiData?.emp_id) {
              this.EMP_ID = apiData.emp_id;
              console.log('✅ emp_id from API:', this.EMP_ID);
            }

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
            this.buildQuestionNavigation(); // NEW: Build navigation
            this.loadQuestion(0); // NEW: Load first question
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
  // ✅ Start with duration from instructions (already loaded)
  let minutes = this.durationInMinutes;

  // ✅ Override with API response if available (API takes priority)
  if (response[0]?.duration) {
    minutes = response[0].duration;
  } else if (response.duration) {
    minutes = response.duration;
  }

  // ✅ Update all duration-related properties
  this.durationInMinutes = minutes;
  this.timeLeft = minutes * 60;
  this.timerDisplay = this.formatTime(this.timeLeft);

  console.log(`✅ Test Duration: ${minutes} minutes`);
  console.log(`✅ Time Left in seconds: ${this.timeLeft}`);
  this.cdr.markForCheck();
}





  private transformResponse(parsedQuestions: any, response: any): QuestionsResponse {
    return {
      test_id: response.test_id || response[0]?.test_id,
      q_id: response.q_id || response[0]?.q_id,
      emp_code: response.emp_code || response[0]?.emp_code,
      people: 1,
      'person 1': {
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

  private generatePersonIndices(): void {
    if (!this.questions) {
      this.personIndices = [];
      return;
    }
    this.personIndices = Array.from({ length: this.questions.people }, (_, i) => i);
  }

  // NEW: Build question navigation array
  private buildQuestionNavigation(): void {
    this.questionNavigation = [];
    if (!this.currentPersonData) return;

    let globalIndex = 0;

    // Add MCQ questions
    this.currentPersonData.mcq?.forEach((_, idx) => {
      this.questionNavigation.push({
        index: globalIndex++,
        type: 'mcq',
        questionIndex: idx,
        isAnswered: false
      });
    });

    // Add True/False questions
    this.currentPersonData['true/false']?.forEach((_, idx) => {
      this.questionNavigation.push({
        index: globalIndex++,
        type: 'true/false',
        questionIndex: idx,
        isAnswered: false
      });
    });

    // Add Fill in the Blanks questions
    this.currentPersonData['fill in the blanks']?.forEach((_, idx) => {
      this.questionNavigation.push({
        index: globalIndex++,
        type: 'fill in the blanks',
        questionIndex: idx,
        isAnswered: false
      });
    });

    // Add Scenario questions
    this.currentPersonData.scenario?.forEach((_, idx) => {
      this.questionNavigation.push({
        index: globalIndex++,
        type: 'scenario',
        questionIndex: idx,
        isAnswered: false
      });
    });

    this.updateNavigationStatus();
  }

  // NEW: Update navigation status based on answers
  private updateNavigationStatus(): void {
    this.questionNavigation.forEach(nav => {
      const answer = this.getCurrentAnswer(nav.type, nav.questionIndex);
      nav.isAnswered = answer !== null && answer !== undefined && answer.trim() !== '';
    });
    this.cdr.markForCheck();
  }

  // NEW: Load specific question by index
  loadQuestion(index: number): void {
    if (index < 0 || index >= this.questionNavigation.length) return;

    this.currentQuestionIndex = index;
    const nav = this.questionNavigation[index];
    const personData = this.currentPersonData;

    if (!personData) return;

    switch (nav.type) {
      case 'mcq':
        this.currentQuestion = {
          ...personData.mcq![nav.questionIndex],
          type: 'mcq',
          questionIndex: nav.questionIndex
        };
        break;
      case 'true/false':
        this.currentQuestion = {
          ...personData['true/false']![nav.questionIndex],
          type: 'true/false',
          questionIndex: nav.questionIndex
        };
        break;
      case 'fill in the blanks':
        this.currentQuestion = {
          ...personData['fill in the blanks']![nav.questionIndex],
          type: 'fill in the blanks',
          questionIndex: nav.questionIndex
        };
        break;
      case 'scenario':
        this.currentQuestion = {
          ...personData.scenario![nav.questionIndex],
          type: 'scenario',
          questionIndex: nav.questionIndex
        };
        break;
    }

    this.cdr.markForCheck();
  }

  get currentPersonData(): PersonData | null {
    if (!this.questions) return null;
    const data = this.questions[`person ${this.currentPersonIndex + 1}`];
    return data as PersonData || null;
  }

  getOptionValue(question: any, optNum: number): string {
    return question[`option ${optNum}`] || '';
  }

  getCurrentAnswer(type: keyof UserAnswersData, index: number): string {
    return this.userAnswers[this.currentPersonIndex]?.[type]?.[index] || '';
  }

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
    this.updateNavigationStatus();
    this.updateStats();
    this.cdr.markForCheck();
  }

  private updateStats(): void {
    this.unAttemptedCount = this.getUnAttemptedCount();
    this.attemptedCount = this.getAttemptedCount();
    this.cdr.markForCheck();
  }

  private getUnAttemptedCount(): number {
    if (!this.currentPersonData) return 0;

    const currentAnswers = this.userAnswers[this.currentPersonIndex];
    if (!currentAnswers) return 0;

    let unattempted = 0;

    currentAnswers.mcq.forEach((ans) => {
      if (!ans || ans.trim() === '') unattempted++;
    });

    currentAnswers['true/false'].forEach((ans) => {
      if (!ans || ans.trim() === '') unattempted++;
    });

    currentAnswers['fill in the blanks'].forEach((ans) => {
      if (!ans || ans.trim() === '') unattempted++;
    });

    currentAnswers.scenario.forEach((ans) => {
      if (!ans || ans.trim() === '') unattempted++;
    });

    return unattempted;
  }

  private getAttemptedCount(): number {
    if (!this.currentPersonData) return 0;

    const totalQuestions =
      (this.currentPersonData.mcq?.length || 0) +
      (this.currentPersonData['true/false']?.length || 0) +
      (this.currentPersonData['fill in the blanks']?.length || 0) +
      (this.currentPersonData.scenario?.length || 0);

    return totalQuestions - this.getUnAttemptedCount();
  }

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

  private stopTimer(): void {
    if (this.timerSubscription) {
      this.timerSubscription.unsubscribe();
      this.timerSubscription = null;
    }
  }

  private buildResponsePayload(): any {
    const currentAnswers = this.userAnswers[this.currentPersonIndex];
    const currentQuestions = this.currentPersonData;

    if (!currentAnswers || !currentQuestions) {
      console.warn('No answers or questions found');
      return null;
    }

    const personData: any = {
      mcq: [],
      scenario: [],
      'true/false': [],
      'fill in the blanks': []
    };

    if (currentQuestions.mcq && currentAnswers.mcq) {
      personData.mcq = currentQuestions.mcq.map((question: any, index: number) => ({
        question: question.question || '',
        'option 1': question['option 1'] || '',
        'option 2': question['option 2'] || '',
        'option 3': question['option 3'] || '',
        'option 4': question['option 4'] || '',
        answer: question.answer || '',
        user_answer: currentAnswers.mcq[index] || null
      }));
    }

    if (currentQuestions.scenario && currentAnswers.scenario) {
      personData.scenario = currentQuestions.scenario.map((question: any, index: number) => ({
        question: question.question || '',
        user_answer: currentAnswers.scenario[index] || null
      }));
    }

    if (currentQuestions['true/false'] && currentAnswers['true/false']) {
      personData['true/false'] = currentQuestions['true/false'].map((question: any, index: number) => ({
        question: question.question || '',
        'option 1': 'True',
        'option 2': 'False',
        answer: question.answer || '',
        user_answer: currentAnswers['true/false'][index] || null
      }));
    }

    if (currentQuestions['fill in the blanks'] && currentAnswers['fill in the blanks']) {
      personData['fill in the blanks'] = currentQuestions['fill in the blanks'].map((question: any, index: number) => ({
        question: question.question || '',
        answer: question.answer || '',
        user_answer: currentAnswers['fill in the blanks'][index] || null
      }));
    }
    return {
      people: 1,
      'person 1': personData
    };
  }

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
            this.isSubmitting = false;
            this.cdr.markForCheck();
          },
          error: (err) => {
            this.handleSubmitError(err);
            this.isSubmitting = false;
            this.cdr.markForCheck();
          }
        });
    } catch (error: any) {
      this.error = true;
      this.errorMessage = `Error: ${error.message}`;
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
      emp_id: this.EMP_ID,
      submitted_at: new Date(),
      result: apiResponse,
      attempts: apiResponse.attempted || 1,
      test_name:apiResponse.test_name || this.testTitle
    });

    this.router.navigate(['/test-results']);
  }

  switchPerson(index: number): void {
    this.currentPersonIndex = index;
    this.updateStats();
    window.scrollTo({ top: 0, behavior: 'smooth' });
    this.cdr.markForCheck();
  }

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

    if (this.currentPersonData.mcq && this.currentPersonData.mcq.length > 0) {
      const unansweredMcq = currentAnswers.mcq.some(ans => !ans || ans.trim() === '');
      if (unansweredMcq) return false;
    }

    if (this.currentPersonData['true/false'] && this.currentPersonData['true/false'].length > 0) {
      const unansweredTF = currentAnswers['true/false'].some(ans => !ans || ans.trim() === '');
      if (unansweredTF) return false;
    }

    if (this.currentPersonData['fill in the blanks'] && this.currentPersonData['fill in the blanks'].length > 0) {
      const unansweredFIB = currentAnswers['fill in the blanks'].some(ans => !ans || ans.trim() === '');
      if (unansweredFIB) return false;
    }

    if (this.currentPersonData.scenario && this.currentPersonData.scenario.length > 0) {
      const unansweredScenario = currentAnswers.scenario.some(ans => !ans || ans.trim() === '');
      if (unansweredScenario) return false;
    }

    return true;
  }

  get totalQuestions(): number {
    if (!this.currentPersonData) return 0;

    return (
      (this.currentPersonData.mcq?.length || 0) +
      (this.currentPersonData['true/false']?.length || 0) +
      (this.currentPersonData['fill in the blanks']?.length || 0) +
      (this.currentPersonData.scenario?.length || 0)
    );
  }

  get submitButtonMessage(): string {
    if (this.allQuestionsAnswered) {
      return 'Submit';
    }
    return `Complete all ${this.unAttemptedCount} unanswered question(s)`;
  }
}