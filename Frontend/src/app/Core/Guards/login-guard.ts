import { Injectable } from '@angular/core';
import { CanActivate, Router, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoginGuard implements CanActivate {
  constructor(private router: Router) {}

  canActivate(): boolean | UrlTree | Observable<boolean | UrlTree> | Promise<boolean | UrlTree> {
    // Check if user is already logged in
    const isLoggedLocal = typeof window !== 'undefined' && localStorage.getItem('isLoggedIn') === 'true';
    const isLoggedSession = typeof window !== 'undefined' && sessionStorage.getItem('isLoggedIn') === 'true';

    if (isLoggedLocal || isLoggedSession) {
      // User is already logged in, redirect to dashboard/history
      return this.router.createUrlTree(['/history']);
    }

    // User is not logged in, allow access to login page
    return true;
  }
}