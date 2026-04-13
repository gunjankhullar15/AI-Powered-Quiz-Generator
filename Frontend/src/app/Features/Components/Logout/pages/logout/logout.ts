import { Component } from '@angular/core';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-logout',
  imports: [],
  templateUrl: './logout.html',
  styleUrl: './logout.scss',
})
export class Logout {

  // constructor(
  //   private router: Router
  // ) {}

  // onLogout(): void {
  //   Swal.fire({
  //     title: 'Are you sure?',
  //     text: 'You want to logout?',
  //     icon: 'warning',
  //     showCancelButton: true,
  //     confirmButtonColor: '#3085d6',
  //     cancelButtonColor: '#d33',
  //     confirmButtonText: 'Yes, logout!',
  //     cancelButtonText: 'Cancel',
  //     reverseButtons: true
  //   }).then((result) => {
  //     if (result.isConfirmed) {
  //       // Show success message
  //       Swal.fire({
  //         title: 'Logged Out!',
  //         text: 'You have been successfully logged out.',
  //         icon: 'success',
  //         timer: 1500,
  //         showConfirmButton: false
  //       });

  //       // Perform logout actions
  //       this.performLogout();
  //     }
  //   });
  // }

  // private performLogout(): void {
    
  //   setTimeout(() => {
  //     this.router.navigate(['/login']);
  //   }, 1500);
  // }
}