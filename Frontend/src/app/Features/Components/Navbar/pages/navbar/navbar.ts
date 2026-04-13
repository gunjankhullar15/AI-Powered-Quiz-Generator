import { Component } from '@angular/core';
import { MaterialModule } from '../../../../../Shared/Modules/materialModule';
import { Router } from '@angular/router';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { Logout } from '../../../Logout/pages/logout/logout';
import Swal from 'sweetalert2';


@Component({
  selector: 'app-navbar',
  imports: [MaterialModule],
  templateUrl: './navbar.html',
  styleUrl: './navbar.scss',
})
// export class Navbar {



// constructor(
//     private router: Router, 
//     private snackBar: MatSnackBar
//   ) {}

//   openLogoutDialog(): void {
//     // Create logout component instance which will show SweetAlert
//     const logoutComponent = new Logout();
    
//     // The component handles the confirmation internally
//     // We just need to handle the result
//   }

//   logout(): void {
//     // Clear storage
//     localStorage.clear();
//     sessionStorage.clear();

//     this.snackBar.open('Logged out successfully', 'Close', {
//       duration: 2000,
//       horizontalPosition: 'center',
//       verticalPosition: 'bottom'
//     });

//     this.router.navigate(['/login']);
//   }
// }



export class Navbar {
  constructor(
    private router: Router, 
    private snackBar: MatSnackBar
  ) {}

  openLogoutDialog(): void {
    Swal.fire({
      title: 'Are you sure?',
      text: 'You want to logout?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, logout!',
      cancelButtonText: 'Cancel',
      reverseButtons: true
    }).then((result) => {
      if (result.isConfirmed) {
        this.logout();
      }
    });
  }

  logout(): void {
    // Clear storage
    localStorage.clear();
    sessionStorage.clear();

    // Show success message
    Swal.fire({
      title: 'Logged Out!',
      text: 'You have been successfully logged out.',
      icon: 'success',
      timer: 1500,
      showConfirmButton: false
    });

    // Redirect to login page after delay
    setTimeout(() => {
      this.router.navigate(['/login']);
    }, 1500);
  }
}