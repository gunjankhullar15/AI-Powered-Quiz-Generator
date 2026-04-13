import { CreatetestSer } from './../../services/createtestSer';
import { ChangeDetectorRef, Component, OnInit, viewChild } from '@angular/core';
import { MatTableModule } from '@angular/material/table';
import { ViewChild } from '@angular/core';
import { MatPaginator, MatPaginatorModule } from '@angular/material/paginator';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import Swal from 'sweetalert2';
import { MatSnackBar } from '@angular/material/snack-bar';
import {TestForm,WeightageResponse,MarksConfig,CreateTestPayload,CreateTestResponse,DocumentPreviewResponse} from '../../../../../Shared/Interfaces/create-test';
import { MaterialModule } from '../../../../../Shared/Modules/materialModule';
import { Navbar } from '../../../Navbar/pages/navbar/navbar';


@Component({
  selector: 'app-createtest',
  imports: [FormsModule,CommonModule,
    MatTableModule,        // ✅ Added
    MaterialModule,MatPaginatorModule,Navbar],
  templateUrl: './createtest.html',
  styleUrl: './createtest.scss',
})


export class Createtest implements OnInit {
  
  marksConfig: MarksConfig = {
    mcq: 0,
    matchFollowing: 0,
    scenarioBased: 0,
    fillBlanks: 0,
    trueFalse: 0
  };

  form: TestForm = {
    name: '',
    numMCQ: '',
    numMatchFollowing: '',
    numScenarioBased: '',
    numFillBlanks: '',
    numTrueFalse: '',
    duration: '',
    deadline: '',
    passingMarks: 0,
    totalMarks: 0,
    numPeople: '',
    description: '',
    document: null,
    articleLink: '',
    topic: ''
  };

  isDragging = false;
  uploadedFileName: string = '';
  documentType: string = 'upload';
  useAllContent: boolean = false;
  Router: any;
  isDocumentSubmitted: boolean = false;
  isArticleSubmitted: boolean = false;
selectedFiles: FileList | null = null;
  

  constructor(private http: HttpClient, private cdr: ChangeDetectorRef,private router:Router,private create:CreatetestSer) {}

  ngOnInit(): void {
    this.fetchMarksConfiguration();
  }

  fetchMarksConfiguration(): void {
  this.create.getweightage().subscribe({
    next: (response) => {
      response.forEach((item: { weightage: string; question_type: any; }) => {
        const weightage = parseFloat(item.weightage);

        switch (item.question_type) {
          case 'MCQ':
            this.marksConfig.mcq = weightage;
            break;
          case 'Short_Answer':
            this.marksConfig.matchFollowing = weightage;
            break;
          case 'Scenario_Based':
            this.marksConfig.scenarioBased = weightage;
            break;
          case 'Fill_Blanks':
            this.marksConfig.fillBlanks = weightage;
            break;
          case 'True_False':
            this.marksConfig.trueFalse = weightage;
            break;
        }
      });

      // Run change detection and update total marks once after loop
      this.cdr.detectChanges();
      this.calculateTotalMarks();
    },
  });
}


  calculateTotalMarks(): void {
    const mcqMarks = (parseInt(this.form.numMCQ) || 0) * this.marksConfig.mcq;
    const matchMarks = (parseInt(this.form.numMatchFollowing) || 0) * this.marksConfig.matchFollowing;
    const scenarioMarks = (parseInt(this.form.numScenarioBased) || 0) * this.marksConfig.scenarioBased;
    const fillBlanksMarks = (parseInt(this.form.numFillBlanks) || 0) * this.marksConfig.fillBlanks;
    const trueFalseMarks = (parseInt(this.form.numTrueFalse) || 0) * this.marksConfig.trueFalse;

    this.form.totalMarks = mcqMarks + matchMarks + scenarioMarks + fillBlanksMarks + trueFalseMarks;
  }

  // onQuestionTypeChange(): void {
  //   this.form.numMCQ = this.validateInput(this.form.numMCQ);
  //   this.form.numMatchFollowing = this.validateInput(this.form.numMatchFollowing);
  //   this.form.numScenarioBased = this.validateInput(this.form.numScenarioBased);
  //   this.form.numFillBlanks = this.validateInput(this.form.numFillBlanks);
  //   this.form.numTrueFalse = this.validateInput(this.form.numTrueFalse);
    
  //   this.calculateTotalMarks();
  // }

  // validateInput(value: string): string {
  //   const num = parseInt(value);
  //   if (isNaN(num) || num < 0) {
  //     return '';
  //   }
  //   return value;
  // }
onQuestionTypeChange(): void {
  this.form.numMCQ = this.validateInput(this.form.numMCQ, 1, 25);
  this.form.numMatchFollowing = this.validateInput(this.form.numMatchFollowing, 1, 25);
  this.form.numScenarioBased = this.validateInput(this.form.numScenarioBased, 1, 25);
  this.form.numFillBlanks = this.validateInput(this.form.numFillBlanks, 1, 25);
  this.form.numTrueFalse = this.validateInput(this.form.numTrueFalse, 1, 25);
  
  this.calculateTotalMarks();
}


  validateInput(value: string, min: number = 0, max: number = 25): string {
  const num = parseInt(value);
  if (isNaN(num) || num < min) {
    return '';
  }
  if (num > max) {
    return max.toString();
  }
  return value;
}



onDurationChange(): void {
  const duration = parseInt(this.form.duration);
  if (isNaN(duration) || duration < 5) {
    this.form.duration = '';
  } else if (duration > 300) {
    this.form.duration = '300';
  }
}

onNumPeopleChange(): void {
  const numPeople = parseInt(this.form.numPeople);
  if (isNaN(numPeople) || numPeople < 1) {
    this.form.numPeople = '';
  } else if (numPeople > 100) {
    this.form.numPeople = '100';
  }
}







  onDocumentTypeChange(): void {
    // Prevent changing if already submitted
    // if (this.documentType === 'upload' && this.isArticleSubmitted) {
    //   Swal.fire({
    //     icon: 'warning',
    //     title: 'Cannot Switch',
    //     text: 'Article has already been submitted. Please discard it first.',
    //     confirmButtonColor: '#ff6b35'
    //   });
    //   this.documentType = 'article';
    //   return;
    // }
    
    // if (this.documentType === 'article' && this.isDocumentSubmitted) {
    //   Swal.fire({
    //     icon: 'warning',
    //     title: 'Cannot Switch',
    //     text: 'Document has already been submitted. Please discard it first.',
    //     confirmButtonColor: '#ff6b35'
    //   });
    //   this.documentType = 'upload';
    //   return;
    // }
  }
    
    // Clear the other option when switching
  //   if (this.documentType === 'upload') {
  //     this.form.articleLink = '';
  //     this.isArticleSubmitted = false;
  //   } else {
  //     this.form.document = null;
  //     this.uploadedFileName = '';
  //     this.isDocumentSubmitted = false;
  //   }
  // }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;

    if (event.dataTransfer?.files && event.dataTransfer.files.length > 0) {
      this.handleFiles(event.dataTransfer.files);
    } else {
      Swal.fire({
        icon: 'info',
        title: 'Note',
        text: 'Please use the Upload button to select a folder',
        confirmButtonColor: '#ff6b35'
      });
    }
  }

  onFileSelect(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.handleFiles(input.files);
    }
  }

  








  



handleFiles(files: FileList): void {
  if (files.length === 0) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'No files selected',
      confirmButtonColor: '#ff6b35'
    });
    return;
  }

  // Store all files from the folder
  const fileArray = Array.from(files);
  const validFormats = ['pdf', 'ppt', 'pptx', 'docx', 'doc', 'txt'];
  
  // Validate all files have valid formats
  const invalidFiles = fileArray.filter(file => {
    const fileName = file.name.toLowerCase();
    const fileExt = fileName.split('.').pop()?.toLowerCase();
    const isValidExtension = fileExt && validFormats.includes(fileExt);
    const isValidMIME = this.isValidMimeType(file.type);
    
    return !isValidExtension && !isValidMIME;
  });

  if (invalidFiles.length > 0) {
    const invalidFileNames = invalidFiles.map(f => f.name).join(', ');
    Swal.fire({
      icon: 'error',
      title: 'Invalid Files',
      text: `Invalid files: ${invalidFileNames}. Only PDF, PPT, PPTX, DOCX, DOC, and TXT are allowed.`,
      confirmButtonColor: '#ff6b35'
    });
    return;
  }

  // Store the FileList
  this.selectedFiles = files;
  this.form.document = files[0];
  
  // Show folder name or file count
  if (files.length > 1) {
    this.uploadedFileName = `${files.length} files selected`;
  } else {
    this.uploadedFileName = files[0].name;
  }
  
  console.log('Files uploaded:', fileArray.map(f => f.name));
}






// Add this helper method to validate MIME types
private isValidMimeType(mimeType: string): boolean {
  const validMimeTypes = [
    'application/pdf',
    'application/vnd.ms-powerpoint',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation', // .pptx
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document', // .docx
    'application/msword', // .doc
    'text/plain'
  ];
  
  return validMimeTypes.some(mime => mimeType.includes(mime));
}

  triggerFileInput(): void {
    const fileInput = document.getElementById('fileInput') as HTMLInputElement;
    if (fileInput) {
      fileInput.click();
    }
  }



discardFile(): void {
  this.form.document = null;
  this.uploadedFileName = '';
  this.isDocumentSubmitted = false;
  this.selectedFiles = null;  // Add this line
  const fileInput = document.getElementById('fileInput') as HTMLInputElement;
  if (fileInput) {
    fileInput.value = '';
  }
}


  //  deleteSubmittedDocument(): void {
    
    
  // console.log('🔴 deleteSubmittedDocument() CALLED');
  // console.log('Current state:', {
  //   isDocumentSubmitted: this.isDocumentSubmitted,
  //   uploadedFileName: this.uploadedFileName,
  //   hasDocument: !!this.form.document
  // });
    
    
  //   Swal.fire({
  //     title: 'Are you sure?',
  //     text: 'Do you want to delete the submitted document?',
  //     icon: 'warning',
  //     showCancelButton: true,
  //     confirmButtonColor: '#ff6b35',
  //     cancelButtonColor: '#6c757d',
  //     confirmButtonText: 'Yes, delete it!',
  //     cancelButtonText: 'Cancel'
  //   }).then((result) => {
  //     if (result.isConfirmed) {
  //       this.callDeleteAPI();
  //     }
  //     else {
  //     console.log('🔴 User cancelled deletion');
  //   }
  //   });
  // }


  deleteSubmittedDocument(): void {
  Swal.fire({
    title: 'Are you sure?',
    text: 'Do you want to delete the submitted document?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ff6b35',
    cancelButtonColor: '#6c757d',
    confirmButtonText: 'Yes, delete it!',
    cancelButtonText: 'Cancel'
  }).then((result) => {
    if (result.isConfirmed) {
      this.callDeleteAPI('document');
    }
  });
}

  // deleteSubmittedArticle(): void {
    
  //    console.log('🟡 deleteSubmittedArticle() CALLED');
  // console.log('Current state:', {
  //   isArticleSubmitted: this.isArticleSubmitted,
  //   articleLink: this.form.articleLink
  // });
    
  //   Swal.fire({
  //     title: 'Are you sure?',
  //     text: 'Do you want to delete the submitted article?',
  //     icon: 'warning',
  //     showCancelButton: true,
  //     confirmButtonColor: '#ff6b35',
  //     cancelButtonColor: '#6c757d',
  //     confirmButtonText: 'Yes, delete it!',
  //     cancelButtonText: 'Cancel'
  //   }).then((result) => {
  //     if (result.isConfirmed) {
  //       this.callDeleteAPI();
  //     }
  //     else {
  //     console.log('🟡 User cancelled deletion');
  //   }
  //   });
  // }


deleteSubmittedArticle(): void {
  Swal.fire({
    title: 'Are you sure?',
    text: 'Do you want to delete the submitted article?',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#ff6b35',
    cancelButtonColor: '#6c757d',
    confirmButtonText: 'Yes, delete it!',
    cancelButtonText: 'Cancel'
  }).then((result) => {
    if (result.isConfirmed) {
      this.callDeleteAPI('article');
    }
  });
}




// callDeleteAPI(): void {
//   console.log('🟢 callDeleteAPI() CALLED - THIS IS THE MOST IMPORTANT LOG');
//   console.log('🟢 About to show loading Swal');
  
//   // Show loading
//   Swal.fire({
//     title: 'Deleting...',
//     text: 'Please wait',
//     allowOutsideClick: false,
//     didOpen: () => {
//       console.log('🟢 Loading Swal opened');
//       Swal.showLoading();
//     }
//   });

//   console.log('🟢 About to call this.create.deleteTest()');
//   console.log('🟢 Service instance:', this.create);
  
//   const deleteObservable = this.create.deleteTest();
//   console.log('🟢 Observable created:', deleteObservable);
  
//   deleteObservable.subscribe({
//     next: (response) => {
//       console.log('✅ DELETE SUCCESS - Response:', response);
      
//       // Reset both document and article states completely
//       this.form.document = null;
//       this.uploadedFileName = '';
//       this.isDocumentSubmitted = false;
//       this.form.articleLink = '';
//       this.isArticleSubmitted = false;
//       this.selectedFiles = null;
      
//       // Reset to default document type (upload)
//       this.documentType = 'upload';
      
//       // Clear file input
//       const fileInput = document.getElementById('fileInput') as HTMLInputElement;
//       if (fileInput) {
//         fileInput.value = '';
//       }

//       // Trigger change detection to update the UI
//       this.cdr.detectChanges();

//       Swal.fire({
//         icon: 'success',
//         title: 'Deleted!',
//         text: 'Content has been deleted successfully. You can now upload new content.',
//         timer: 2000,
//         showConfirmButton: false
//       });
//     },
//     error: (error) => {
//       console.error('❌ DELETE ERROR - Full error object:', error);
//       console.error('❌ Error status:', error.status);
//       console.error('❌ Error statusText:', error.statusText);
//       console.error('❌ Error message:', error.message);
//       console.error('❌ Error url:', error.url);
      
//       Swal.fire({
//         icon: 'error',
//         title: 'Delete Failed',
//         text: error.error?.detail || error.message || 'Failed to delete content. Please try again.',
//         confirmButtonColor: '#ff6b35'
//       });
//     },
//     complete: () => {
//       console.log('🏁 DELETE OBSERVABLE COMPLETED');
//     }
//   });
  
//   console.log('🟢 Subscribe called - waiting for response...');
// }
































  
  


// onSubmitDocument(): void {
//   if (!this.selectedFiles || this.selectedFiles.length === 0) {
//     Swal.fire({
//       icon: 'error',
//       title: 'Error',
//       text: 'Please select a file first',
//       confirmButtonColor: '#ff6b35'
//     });
//     return;
//   }

//   // Call document preview API with FileList
//   this.callDocumentPreviewAPI(this.selectedFiles);
  
//   // Mark document as submitted and disable article option
//   this.isDocumentSubmitted = true;
  
//   Swal.fire({
//     icon: 'success',
//     title: 'Document Submitted',
//     text: 'Document(s) submitted successfully.',
//     timer: 2000,
//     showConfirmButton: false
//   });
// }

callDeleteAPI(type: string): void {
  Swal.fire({
    title: 'Deleting...',
    text: 'Please wait',
    allowOutsideClick: false,
    didOpen: () => {
      Swal.showLoading();
    }
  });

  this.create.deleteTest().subscribe({
    next: (response) => {
      // Reset only the specific item being deleted
      if (type === 'document') {
        this.form.document = null;
        this.uploadedFileName = '';
        this.isDocumentSubmitted = false;
        this.selectedFiles = null;
      } else if (type === 'article') {
        this.form.articleLink = '';
        this.isArticleSubmitted = false;
      }
      
      const fileInput = document.getElementById('fileInput') as HTMLInputElement;
      if (fileInput) {
        fileInput.value = '';
      }

      this.cdr.detectChanges();

      Swal.fire({
        icon: 'success',
        title: 'Deleted!',
        text: 'Content has been deleted successfully. You can now upload new content.',
        timer: 2000,
        showConfirmButton: false
      });
    },
    error: (error) => {
      Swal.fire({
        icon: 'error',
        title: 'Delete Failed',
        text: error.error?.detail || error.message || 'Failed to delete content. Please try again.',
        confirmButtonColor: '#ff6b35'
      });
    }
  });
}

// onSubmitDocument(): void {
//   if (!this.selectedFiles || this.selectedFiles.length === 0) {
//     Swal.fire({
//       icon: 'error',
//       title: 'Error',
//       text: 'Please select a file first',
//       confirmButtonColor: '#ff6b35'
//     });
//     return;
//   }
// }


onSubmitDocument(): void {
  if (!this.selectedFiles || this.selectedFiles.length === 0) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Please select a file first',
      confirmButtonColor: '#ff6b35'
    });
    return;
  }

  Swal.fire({
    title: 'Submitting...',
    text: 'Please wait',
    allowOutsideClick: false,
    didOpen: () => {
      Swal.showLoading();
    }
  });

  this.callDocumentPreviewAPI(this.selectedFiles);
}

  onDiscardArticle(): void {
    this.form.articleLink = '';
    this.isArticleSubmitted = false;
  }



  // onSubmitArticle(): void {
  //   if (!this.form.articleLink || !this.form.articleLink.trim()) {
  //     Swal.fire({
  //       icon: 'error',
  //       title: 'Error',
  //       text: 'Please enter an article URL',
  //       confirmButtonColor: '#ff6b35'
  //     });
  //     return;
  //   }

  //   // Call article preview API
  //   this.callArticlePreviewAPI(this.form.articleLink);
    
  //   // Mark article as submitted and disable document option
  //   this.isArticleSubmitted = true;
    
  //   Swal.fire({
  //     icon: 'success',
  //     title: 'Article Submitted',
  //     text: 'Article URL has been submitted successfully.',
  //     timer: 2000,
  //     showConfirmButton: false
  //   });
  // }
onSubmitArticle(): void {
  if (!this.form.articleLink || !this.form.articleLink.trim()) {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Please enter an article URL',
      confirmButtonColor: '#ff6b35'
    });
    return;
  }

  Swal.fire({
    title: 'Submitting...',
    text: 'Please wait',
    allowOutsideClick: false,
    didOpen: () => {
      Swal.showLoading();
    }
  });

  this.callArticlePreviewAPI(this.form.articleLink);
}

// callDocumentPreviewAPI(files: FileList): void {
//   try {
//     const fileArray = Array.from(files);
    
    
//     // Pass single file or array based on count
//     const filesToSend = fileArray.length === 1 ? fileArray[0] : fileArray;
    
   
//     this.create.onsubmitdoc(filesToSend).subscribe({
//       next: (response) => {
//         console.log('Document preview loaded:', response);
//         Swal.fire({
//           icon: 'success',
//           title: 'Success',
//           text: typeof response === 'string' ? response : 'Files processed successfully',
//           timer: 2000,
//           showConfirmButton: false
//         });
//       },
//       error: (error) => {
//         Swal.fire({
//           icon: 'error',
//           title: 'Error',
//           text: error.error?.detail || 'Failed to process document(s)',
//           confirmButtonColor: '#ff6b35'
//         });
//       }
//     });
//   } catch (err) {
//     console.error('Error in document preview:', err);
//   }
// }
callDocumentPreviewAPI(files: FileList): void {
  try {
    const fileArray = Array.from(files);
    const filesToSend = fileArray.length === 1 ? fileArray[0] : fileArray;
    
    this.create.onsubmitdoc(filesToSend).subscribe({
      next: (response) => {
        console.log('Document preview loaded:', response);
        this.isDocumentSubmitted = true;
        
        Swal.fire({
          icon: 'success',
          title: 'Success',
          text: 'Document(s) submitted successfully',
          timer: 2000,
          showConfirmButton: false
        });
      },
      error: (error) => {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: error.error?.detail || 'Failed to process document(s)',
          confirmButtonColor: '#ff6b35'
        });
      }
    });
  } catch (err) {
    console.error('Error in document preview:', err);
  }
}


// callArticlePreviewAPI(articleUrl: string): void {
//   try {
//     this.create.onsubmitarticle(articleUrl).subscribe({
//       next: (response) => {
//         console.log('Article preview loaded:', response);
//         Swal.fire({
//           icon: 'success',
//           title: 'Success',
//           text: 'Article processed successfully',
//           timer: 2000,
//           showConfirmButton: false
//         });
//       },
//       error: (error) => {
//         console.error('Error loading article preview:', error);
//         Swal.fire({
//           icon: 'error',
//           title: 'Error',
//           text: error.error?.detail || 'Failed to process article',
//           confirmButtonColor: '#ff6b35'
//         });
//       }
//     });
//   } catch (err) {
//     console.error('Error in article preview:', err);
//   }
// }
callArticlePreviewAPI(articleUrl: string): void {
  try {
    this.create.onsubmitarticle(articleUrl).subscribe({
      next: (response) => {
        console.log('Article preview loaded:', response);
        this.isArticleSubmitted = true;
        
        Swal.fire({
          icon: 'success',
          title: 'Success',
          text: 'Article submitted successfully',
          timer: 2000,
          showConfirmButton: false
        });
      },
      error: (error) => {
        console.error('Error loading article preview:', error);
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: error.error?.detail || 'Failed to process article',
          confirmButtonColor: '#ff6b35'
        });
      }
    });
  } catch (err) {
    console.error('Error in article preview:', err);
  }
}

  onArticleLinkChange(): void {
    // Call preview API when article link is provided
    if (this.form.articleLink && this.form.articleLink.trim()) {
      this.callArticlePreviewAPI(this.form.articleLink);
    }
  }


onCreateTest(): void {
    // Validation checks
    if (!this.form.name || !this.form.description) {
      Swal.fire({
        icon: 'error',
        title: 'Validation Error',
        text: 'Please fill in test name and description',
        confirmButtonColor: '#ff6b35'
      });
      return;
    }

     if (!this.isDocumentSubmitted && !this.isArticleSubmitted) {
      Swal.fire({
        icon: 'error',
        title: 'Validation Error',
        text: 'Please submit either a document or article URL before creating the test',
        confirmButtonColor: '#ff6b35'
      });
      return;
    }

    if (this.form.totalMarks === 0) {
      Swal.fire({
        icon: 'error',
        title: 'Validation Error',
        text: 'Please select at least one question type',
        confirmButtonColor: '#ff6b35'
      });
      return;
    }
    
    if (this.form.passingMarks > this.form.totalMarks) {
      Swal.fire({
        icon: 'error',
        title: 'Validation Error',
        text: 'Passing marks cannot exceed total marks',
        confirmButtonColor: '#ff6b35'
      });
      return;
    }

    if (!this.form.duration) {
      Swal.fire({
        icon: 'error',
        title: 'Validation Error',
        text: 'Please enter test duration',
        confirmButtonColor: '#ff6b35'
      });
      return;
    }

    if (!this.form.deadline) {
      Swal.fire({
        icon: 'error',
        title: 'Validation Error',
        text: 'Please select a deadline',
        confirmButtonColor: '#ff6b35'
      });
      return;
    }

    const mcqNum = parseInt(this.form.numMCQ) || 0;
    const matchNum = parseInt(this.form.numMatchFollowing) || 0;
    const scenarioNum = parseInt(this.form.numScenarioBased) || 0;
    const fillBlanksNum = parseInt(this.form.numFillBlanks) || 0;
    const trueFalseNum = parseInt(this.form.numTrueFalse) || 0;

    if (mcqNum > 25 || matchNum > 25 || scenarioNum > 25 || fillBlanksNum > 25 || trueFalseNum > 25) {
      Swal.fire({
        icon: 'error',
        title: 'Validation Error',
        text: 'Maximum 25 questions allowed per question type',
        confirmButtonColor: '#ff6b35'
      });
      return;
    }

    // Validate duration
    const duration = parseInt(this.form.duration);
    if (duration < 5 || duration > 300) {
      Swal.fire({
        icon: 'error',
        title: 'Validation Error',
        text: 'Duration must be between 5 and 300 minutes',
        confirmButtonColor: '#ff6b35'
      });
      return;
    }

    // Validate passing marks
    if (this.form.passingMarks < 10) {
      Swal.fire({
        icon: 'error',
        title: 'Validation Error',
        text: 'Passing marks must be at least 10',
        confirmButtonColor: '#ff6b35'
      });
      return;
    }

    // Validate topic if useAllContent is not checked
    if (!this.useAllContent && !this.form.topic) {
      Swal.fire({
        icon: 'error',
        title: 'Validation Error',
        text: 'Please enter a topic or check "Use all content"',
        confirmButtonColor: '#ff6b35'
      });
      return;
    }

    // Show loading
    Swal.fire({
      title: 'Creating Test...',
      text: 'Please wait while we generate your test',
      allowOutsideClick: false,
      didOpen: () => {
        Swal.showLoading();
      }
    });

    // Prepare payload according to API schema
    const payload: CreateTestPayload = {
      topic: this.useAllContent ? 'All Content' : this.form.topic,
      test_name: this.form.name,
      description: this.form.description,
      due_date: new Date(this.form.deadline).toISOString(),
      no_of_mcq: parseInt(this.form.numMCQ) || 0,
      no_scenario_based: parseInt(this.form.numScenarioBased) || 0,
      no_of_fill_blanks: parseInt(this.form.numFillBlanks) || 0,
      no_of_true_false: parseInt(this.form.numTrueFalse) || 0,
      duration: parseInt(this.form.duration) || 0,
      max_marks: this.form.totalMarks,
      passing_marks: this.form.passingMarks,
      no_of_people: parseInt(this.form.numPeople) || 0,
      created_at: new Date().toISOString(),
    };

    this.create.oncreatetest(payload).subscribe({
      next: (response) => {
        console.log('Test created successfully:', response);
        // Extract test link from response
        let testLink = '';
        
        if (typeof response === 'string') {
          testLink = response;
        } else if (response.test && response.test.test_url) {
          // Extract from nested test object
          testLink = response.test.test_url;
        } else if (response.testLink || response.link || response.url || response.test_link || response.test_url) {
          // Fallback to direct properties
          testLink = response.testLink || response.link || response.url || response.test_link || response.test_url;
        }
        
        if (testLink) {
          this.showTestLinkPopup(testLink);
        } else {
          Swal.fire({
            icon: 'success',
            title: 'Test Created!',
            text: response.message || 'Your test has been created successfully',
            confirmButtonColor: '#ff6b35'
          }).then(() => {
            this.router.navigate(['/history']);
          });
        }
      },
      error: (error) => {
        console.error('Error creating test:', error);
        const errorMessage = error.error?.message || error.message || 'Failed to create test. Please try again.';
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: errorMessage,
          confirmButtonColor: '#ff6b35'
        });
      }
    });
  }

  showTestLinkPopup(testLink: string): void {
    Swal.fire({
      title: 'Test Link Generated',
      html: `
        <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin: 20px 0;">
          <input 
            id="test-link-input" 
            type="text" 
            value="${testLink}" 
            readonly 
            style="
              flex: 1;
              padding: 10px 15px;
              border: 1px solid #ddd;
              border-radius: 4px;
              font-size: 14px;
              background-color: #ffffff;
              color: #333;
              outline: none;
            "
          />
          <button
            id="copy-btn"
            style="
              padding: 10px 24px;
              background-color: #ff6b35;
              color: white;
              border: none;
              border-radius: 4px;
              font-size: 14px;
              font-weight: 500;
              cursor: pointer;
              transition: background-color 0.2s;
            "
            onmouseover="this.style.backgroundColor='#ff5520'"
            onmouseout="this.style.backgroundColor='#ff6b35'"
          >
            Copy
          </button>
        </div>
      `,
      showConfirmButton: false,
      showCancelButton: false,
      showCloseButton: true,
      width: '600px',
      customClass: {
        popup: 'test-link-popup',
        closeButton: 'swal-close-button'
      },
      didOpen: () => {
        const input = document.getElementById('test-link-input') as HTMLInputElement;
        const copyBtn = document.getElementById('copy-btn') as HTMLButtonElement;
        
        if (input) {
          input.addEventListener('click', () => {
            input.select();
          });
        }
        
        if (copyBtn) {
          copyBtn.addEventListener('click', () => {
            this.copyToClipboard(testLink);
          });
        }
      }
    });
  }

  copyToClipboard(text: string): void {
    navigator.clipboard.writeText(text).then(() => {
      Swal.fire({
        icon: 'success',
        title: 'Copied!',
        text: 'Test link has been copied to clipboard',
        timer: 1500,
        showConfirmButton: false,
        toast: true,
        position: 'top-end'
      });
    }).catch((error) => {
      console.error('Failed to copy:', error);
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = text;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      document.body.appendChild(textArea);
      textArea.select();
      try {
        document.execCommand('copy');
        Swal.fire({
          icon: 'success',
          title: 'Copied!',
          text: 'Test link has been copied to clipboard',
          timer: 1500,
          showConfirmButton: false,
          toast: true,
          position: 'top-end'
        });
      } catch (err) {
        Swal.fire({
          icon: 'error',
          title: 'Copy Failed',
          text: 'Please copy the link manually',
          confirmButtonColor: '#ff6b35'
        });
      }
      document.body.removeChild(textArea);
    });
  }

  onBack(): void {
    this.router.navigate(['/history']);
  }





}










