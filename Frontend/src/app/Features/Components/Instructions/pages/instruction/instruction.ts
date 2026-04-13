import { InstructionsResponse } from './../../../../../Shared/Interfaces/instructionsresponse';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { CommonModule, NgIf } from '@angular/common';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
import { Router } from '@angular/router';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { Navbar } from '../../../Navbar/pages/navbar/navbar';
import { InstructionSer } from '../../services/instruction-ser';
import { TestSer } from '../../../TestPage/services/test-ser';
import { UserNavbar } from '../../../userNavbar/pages/user-navbar/user-navbar';
import { TestPage1Ser } from '../../../TestPage1/services/test-page1-ser';


@Component({
  selector: 'app-instruction',
  imports: [NgIf,CommonModule,HttpClientModule,UserNavbar],
  templateUrl: './instruction.html',
  styleUrl: './instruction.scss',
})

 
export class Instructions implements OnInit {
  instructionsText: string = '';
  formattedInstructions: SafeHtml = '';
  loading = true;
  error: string | null = null;
  // testId: string | null = null;
  testId: string | null = null;
  full_name: string = '';
  emp_code: string = '';
  q_id: string = '';

  constructor(
    private http: HttpClient,
    private route: ActivatedRoute,
    private router: Router,
    private cdr: ChangeDetectorRef,
    private sanitizer: DomSanitizer,
    private inst:InstructionSer,
    private testSer:TestPage1Ser
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.testId = params.get('testId');
    });

    this.route.queryParams.subscribe(queryParams => {
      this.full_name = queryParams['full_name'] || '';
      this.emp_code = queryParams['emp_code'] || '';
//  this.testId = '84';
//   this.emp_code = 'NTs9876';
//   this.full_name = 'piyushJangra1234';
  
//   console.log('Testing with hardcoded values:', {
//     testId: this.testId,
//     emp_code: this.emp_code,
//     full_name: this.full_name
  });
  
      if (this.testId) {
        this.fetchInstructions();
      } else {
        this.error = 'Test ID not provided';
        this.loading = false;
      }
    };

  fetchInstructions(): void {
    console.log('1. fetchInstructions called');
    console.log('2. testId:', this.testId);
    this.loading = true;
    this.error = null;
 if (!this.testId) {
    this.error = 'Test ID not provided';
    this.loading = false;
    return;
  }

    const body = { emp_code: this.emp_code, full_name: this.full_name };
    
    this.inst.getInstructions(this.testId, this.emp_code, this.full_name).subscribe({
      next: (data) => {
        console.log('4. API SUCCESS - Data received:', data);
        console.log('5. Instructions string:', data.instructions);
        this.instructionsText = data.instructions;
        this.q_id = data.q_id.toString();
    this.inst.storeInstructionData(data);


        this.formattedInstructions = this.sanitizer.bypassSecurityTrustHtml(
          this.formatInstructions(data.instructions)
        );
        console.log('6. formattedInstructions:', this.formattedInstructions);
        this.loading = false;
        console.log('7. loading is now:', this.loading);
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('ERROR fetching instructions:', err);
        this.error = 'Failed to load instructions. Please try again.';
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }



onStartTest(): void {
  if (!this.testId || !this.q_id) {
    console.error('Missing test ID or Q ID');
    return;
  }

  this.testSer.storeNavigationState({
    q_id: parseInt(this.q_id),
    test_id: parseInt(this.testId),
    emp_code: this.emp_code,
    full_name: this.full_name
  });
  this.router.navigate(['/test2']);
}

 
  private formatInstructions(text: string): string {
  console.log('Format input:', text);

  let formatted = text.trim();

  // Convert headers (### Text) to <h3> tags only - no bold in content
  formatted = formatted.replace(/### (.*?)$/gm, '<h3>$1</h3>');

  // Remove all bold formatting (**text**) - keep only the text
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '$1');

  // Process numbered lists (1., 2., etc.)
  formatted = formatted.replace(/^\d+\.\s+(.*?)$/gm, '<li>$1</li>');

  // Process bullet points (-)
  formatted = formatted.replace(/^-\s+(.*?)$/gm, '<li>$1</li>');

  // Wrap consecutive list items in <ul>
  formatted = formatted.replace(/(<li>.*?<\/li>[\n]*)+/gs, (match) => {
    const cleaned = match.replace(/\n/g, '');
    if (!cleaned.includes('<ul>')) {
      return '<ul>' + cleaned + '</ul>';
    }
    return cleaned;
  });

  // Split into lines and process
  const lines = formatted.split('\n').filter(line => line.trim());

  formatted = lines
    .map(line => {
      line = line.trim();
      if (!line) return '';

      // Skip if already formatted
      if (
        line.includes('<h3>') ||
        line.includes('<ul>') ||
        line.includes('<li>')
      ) {
        return line;
      }

      // Handle emoji lines
      if (
        line.includes('✅') ||
        line.includes('⏱') ||
        line.includes('🧠') ||
        line.includes('💡')
      ) {
        return '<p class="emoji-text">' + line + '</p>';
      }

      // Wrap regular text in paragraph tags
      return '<p>' + line + '</p>';
    })
    // ✅ JOIN WITHOUT NEWLINES - This removes excess space!
    .join('');

  // ✅ REMOVE MULTIPLE SPACES between tags
  formatted = formatted.replace(/>\s+</g, '><');

  console.log('Format output:', formatted);
  return formatted;
}
}