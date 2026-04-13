import { TestHistory } from './../../../../../Shared/Interfaces/test-history';
import { AfterViewInit, Component, OnInit } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { MaterialModule } from '../../../../../Shared/Modules/materialModule';
import { MatPaginator } from '@angular/material/paginator';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { TesthistorySer } from '../../services/testhistorySer';
import { Logout } from '../../../Logout/pages/logout/logout';
import { Navbar } from '../../../Navbar/pages/navbar/navbar';

@Component({
  selector: 'app-testhistory',
  imports: [FormsModule,CommonModule,
    MaterialModule,Navbar],
  templateUrl: './testhistory.html',
  styleUrl: './testhistory.scss',
})
export class Testhistory implements OnInit, AfterViewInit {
  displayedColumns: string[] = ['sNo', 'testId', 'testname', 'description', 'creationdate', 'duedate', 'testlink'];
  dataSource: MatTableDataSource<TestHistory>;
  
  searchText: string = '';
  selectedDescription: string = '';
  selectedTestId: string = '';
  selectedDueDate:any=null; 
  selectedRow: number | null = null;
  selectedCreationDate: any=null;


 @ViewChild(MatPaginator) paginator!: MatPaginator;



  constructor(private router: Router,private snackBar: MatSnackBar,private http:HttpClient, private dialog: MatDialog,private testSer:TesthistorySer) {
    this.dataSource = new MatTableDataSource<TestHistory>([]);
  }

  // ngOnInit(): void {
  //   this.loadTestHistory();
  // }

ngOnInit(): void {
    this.checkAuthentication();
    this.loadTestHistory();
  }

  private checkAuthentication(): void {
    // Check if user is logged in
    const isLoggedLocal = typeof window !== 'undefined' && localStorage.getItem('isLoggedIn') === 'true';
    const isLoggedSession = typeof window !== 'undefined' && sessionStorage.getItem('isLoggedIn') === 'true';

    if (!isLoggedLocal && !isLoggedSession) {
      // User is not logged in, redirect to login page
      this.router.navigate(['/login']);
    }
  }

ngAfterViewInit() {
  if (this.paginator) {
    this.paginator.pageSize = 10;  // Set default page size here
    this.dataSource.paginator = this.paginator;
  }
}



//   loadTestHistory(): void {


//   this.testSer.getAllTests().subscribe({
//   next: (response: any) => {
//     const tests = Array.isArray(response) ? response : response.data || [];
//     // You can now use 'tests' here


//  const sortedTests = this.sortTestsByCreationDate(tests);

//       this.dataSource.data = sortedTests.map((item: any, index: number) => ({
//         sNo: index + 1,
//         testId: String(item.t_id || ''),
//         testname: item.test_name || '',
//         description: item.description || 'N/A',
//         creationdate: item.creattion_date ? new Date(item.creattion_date).toLocaleDateString() : '',
//         duedate: item.due_date ? new Date(item.due_date).toLocaleDateString() : '',
//         testlink: item.test_url || 'N/A'
//       }));
//   }
// });
//   }


loadTestHistory(): void {
  this.testSer.getAllTests().subscribe({
    next: (response: any) => {
      const tests = Array.isArray(response) ? response : response.data || [];
      const sortedTests = this.sortTestsByCreationDate(tests);

      this.dataSource.data = sortedTests.map((item: any, index: number) => {
        let creationDateStr = '';
        let dueDateStr = '';
        
        if (item.creattion_date) {
          const creationDate = new Date(item.creattion_date);
          creationDateStr = creationDate.toLocaleDateString('en-US');
        }
        
        if (item.due_date) {
          const dueDate = new Date(item.due_date);
          dueDateStr = dueDate.toLocaleDateString('en-US');
        }
        
        return {
          sNo: index + 1,
          testId: String(item.t_id || ''),
          testname: item.test_name || '',
          description: item.description || 'N/A',
          creationdate: creationDateStr,
          duedate: dueDateStr,
          testlink: item.test_url || 'N/A'
        };
      });
    },
    error: (error) => {
      console.error('Error loading test history:', error);
      this.snackBar.open('Failed to load test history', 'Close', { duration: 3000 });
    }
  });
}

  private sortTestsByCreationDate(tests: any[]): any[] {
  return [...tests].sort((a, b) => {
    const dateA = new Date(a.creattion_date).getTime(); // Use actual field name
    const dateB = new Date(b.creattion_date).getTime();
    return dateB - dateA; // Descending order
  });
}



createNewTest(): void {
    console.log('Create new test clicked');
    this.router.navigate(['/test']);
    // Implement navigation or modal logic here
  }

  clearFilters(): void {
    this.searchText = '';
    this.selectedDescription = '';
    this.selectedTestId = '';
    this.selectedCreationDate = null;
    this.selectedDueDate = null;
    this.applyFilter();
  }


applyFilter(): void {
  this.dataSource.filterPredicate = (data: TestHistory, filter: string) => {
    const searchStr = this.searchText.toLowerCase();
    const matchesSearch = !this.searchText || 
      data.testId.toLowerCase().includes(searchStr) ||
      data.testname.toLowerCase().includes(searchStr) ||
      data.description.toLowerCase().includes(searchStr);
    
    const matchesDescription = !this.selectedDescription || 
      data.description === this.selectedDescription;
    
    const matchesTestId = !this.selectedTestId || 
      data.testId === this.selectedTestId;
    
    let matchesCreationDate = true;
    if (this.selectedCreationDate) {
      const selectedDate = new Date(this.selectedCreationDate);
      const selectedDateStr = selectedDate.toLocaleDateString('en-US');
      matchesCreationDate = data.creationdate === selectedDateStr;
    }
    
    let matchesDueDate = true;
    if (this.selectedDueDate) {
      const selectedDate = new Date(this.selectedDueDate);
      const selectedDateStr = selectedDate.toLocaleDateString('en-US');
      matchesDueDate = data.duedate === selectedDateStr;
    }

    return matchesSearch && matchesDescription && matchesTestId && 
           matchesCreationDate && matchesDueDate;
  };
  
  this.dataSource.filter = ' ';
  
  if (this.dataSource.paginator) {
    this.dataSource.paginator.firstPage();
  }
}


  onRowClick(row: TestHistory): void {
  this.selectedRow = row.sNo;
  console.log('Row clicked:', row);
  
  // Pass test data as navigation state
  this.router.navigate(['/candidate',row.testId], {
    state: {
      testId: row.testId,
      testName: row.testname,
      description: row.description,
      creationDate: row.creationdate,
      dueDate: row.duedate,
      testLink: row.testlink
    }
  });
}

  getRowClass(row: TestHistory): string {
    return this.selectedRow === row.sNo ? 'selected-row' : '';
  }



copyTestLink(link: string, event: Event): void {
    event.stopPropagation(); // Prevent row click when copying
    navigator.clipboard.writeText(link).then(() => {
      this.snackBar.open('Test link copied to clipboard!', 'Close', {
        duration: 3000,
        horizontalPosition: 'center',
        verticalPosition: 'bottom'
      });
    }).catch(err => {
      console.error('Failed to copy link:', err);
      this.snackBar.open('Failed to copy link', 'Close', {
        duration: 3000,
        horizontalPosition: 'center',
        verticalPosition: 'bottom'
      });
    });
  }

}