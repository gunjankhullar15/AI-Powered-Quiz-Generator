import { CanActivateFn } from '@angular/router';
import { Injectable } from '@angular/core';
import { CanActivate, Router, UrlTree } from '@angular/router';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
  constructor(private router: Router) {}

  canActivate(): boolean | UrlTree | Observable<boolean | UrlTree> | Promise<boolean | UrlTree> {
    // Check both localStorage and sessionStorage for backward compatibility
    const isLoggedLocal = typeof window !== 'undefined' && localStorage.getItem('isLoggedIn') === 'true';
    const isLoggedSession = typeof window !== 'undefined' && sessionStorage.getItem('isLoggedIn') === 'true';

    if (isLoggedLocal || isLoggedSession) {
      return true;
    }

    // Redirect to the login route when not authenticated
    return this.router.createUrlTree(['/login']);
  }
}