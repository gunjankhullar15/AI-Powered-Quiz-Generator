import { CandidateinfoSer } from './../../services/candidateinfoSer';
import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { ViewChild } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CandidateInfo } from '../../../../../Shared/Interfaces/candidate-info';
import { MaterialModule } from '../../../../../Shared/Modules/materialModule';  
import { Navbar } from '../../../Navbar/pages/navbar/navbar';

@Component({
  selector: 'app-candidateinfo',
  imports: [MaterialModule,FormsModule,CommonModule,Navbar],
  templateUrl: './candidateinfo.html',
  styleUrl: './candidateinfo.scss',
})


export class Candidateinfo implements OnInit {
  displayedColumns: string[] = ['sNo', 'employeeId', 'employeeName', 'score', 'status','attempts'];
  dataSource: MatTableDataSource<CandidateInfo>;
  
  testName: string = 'Java Fundamentals';
  testId: string = '';
  description: string = '';
  creationDate: string = '';
  dueDate: string = '';
  testLink: string = '';

  searchText: string = '';
  selectedEmployeeName: string = '';
  selectedEmployeeId: string = '';
  selectedScore: string = '';
  selectedStatus: string = '';
  
  passCount: number = 0;
  failedCount: number = 0;
  totalCount: number = 0;
  selectedRow: number | null = null;

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(
    private router: Router, 
    private cdr: ChangeDetectorRef,
    private route: ActivatedRoute,
    private http: HttpClient,
    private Candidateinfo: CandidateinfoSer
  ) {
    this.dataSource = new MatTableDataSource<CandidateInfo>([]);
    this.setupFilter(); // Setup filter in constructor
    
    const navigation = this.router.getCurrentNavigation();
    if (navigation?.extras.state) {
      this.loadTestDataFromState(navigation.extras.state);
    }
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      if (params['testId']) {
        this.testId = params['testId'];
        console.log('testId from route params:', this.testId);
      }
    });
    
    const state = history.state;
    if (state && state.testName) {
      this.loadTestDataFromState(state);
    }
    
    console.log('testId before API call:', this.testId);
    
    if (this.testId) {
      this.loadCandidateInfo();
    } else {
      console.error('No testId found - cannot load candidate info');
    }
  }

  loadTestDataFromState(state: any): void {
    this.testId = state.testId || '';
    this.testName = state.testName || 'Java Fundamentals';
    this.description = state.description || '';
    this.creationDate = state.creationDate || '';
    this.dueDate = state.dueDate || '';
    this.testLink = state.testLink || '';
    
    console.log('Loaded test data:', this.testName);
  }

  ngAfterViewInit() {
    if (this.paginator) {
      this.paginator.pageSize = 10;
      this.dataSource.paginator = this.paginator;
      this.cdr.detectChanges();
    }
  }

  setupFilter(): void {
    this.dataSource.filterPredicate = (data: CandidateInfo, filter: string) => {
      const searchStr = this.searchText.toLowerCase().trim();
      
      const matchesSearch = !searchStr || 
        (data.employeeId || '').toLowerCase().includes(searchStr) ||
        (data.employeeName || '').toLowerCase().includes(searchStr);
      
      const matchesStatus = !this.selectedStatus || 
        data.status === this.selectedStatus;
      
      return matchesSearch && matchesStatus;
    };
  }

  loadCandidateInfo(): void {
    console.log('Making API call with testId:', this.testId);
    
    this.Candidateinfo.loadInfo(this.testId).subscribe({
      next: (response: any) => {
        console.log('Candidate Data Response:', response);    
        let data = response.data || response;
        
        if (!Array.isArray(data)) {
          data = [];
        }
        
        const transformedData = data.map((item: any, index: number) => ({
          sNo: index + 1,
          employeeId: item.employee_id || item.employeeId || '',
          employeeName: item.employee_name || item.employeeName || '',
          score: item.score || '0%',
          status: item.status || 'Pending',
           attempts: item.attempted || 0
        }));
        
        console.log('Transformed Data:', transformedData);
        this.dataSource.data = transformedData;
        
        // Re-attach paginator after data load
        setTimeout(() => {
          if (this.paginator) {
            this.dataSource.paginator = this.paginator;
          }
          this.cdr.detectChanges();
        }, 0);
        
        this.calculateStatistics();
      },
      error: (error) => {
        console.error('API Error:', error);
        console.error('API URL was:', `employees/get-candidates/${this.testId}`);
      }
    });
  }

  calculateStatistics(): void {
    const data = this.dataSource.data;
    this.totalCount = data.length;
    this.passCount = data.filter(item => item.status === 'Pass').length;
    this.failedCount = data.filter(item => item.status === 'Fail').length;
  }

  createNewTest(): void {
    console.log('Create new test clicked');
  }

  clearFilters(): void {
    this.searchText = '';
    this.selectedEmployeeName = '';
    this.selectedEmployeeId = '';
    this.selectedScore = '';
    this.selectedStatus = '';
    this.applyFilter();
  }

  applyFilter(): void {
    // Trigger filter by setting a random value
    this.dataSource.filter = Math.random().toString();
    
    if (this.paginator) {
      this.paginator.firstPage();
    }
  }

  onRowClick(row: CandidateInfo): void {
    this.selectedRow = row.sNo;
    console.log('Row clicked:', row);
  }

  getRowClass(row: CandidateInfo): string {
    return this.selectedRow === row.sNo ? 'selected-row' : '';
  }

  goBack(): void {
    this.router.navigate(['/history']);
  }
}











