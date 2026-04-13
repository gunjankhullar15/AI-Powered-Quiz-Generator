import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { catchError } from 'rxjs';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  // Define headers you want to attach
  
  const isFormData = req.body instanceof FormData;

  if (!isFormData) {
  const headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'ngrok-skip-browser-warning': 'true'
  };
 return next(req.clone({ setHeaders: headers })).pipe(
      catchError((error: HttpErrorResponse) => {
        console.error('HTTP Error:', error);
        throw error;
      })
    );
  } else {
    // For FormData, only set non-Content-Type headers
    // Let the browser automatically set Content-Type with proper multipart/form-data boundary
    const headers = {
      'Accept': 'application/json',
      'ngrok-skip-browser-warning': 'true'
    };


  // Clone the request and add headers
  // const clonedRequest = req.clone({ setHeaders: headers });

  // Pass the modified request to the next handler
  // return next(clonedRequest).pipe(
  //   catchError((error:HttpErrorResponse) => {

  //     console.error('HTTP Error:', error);
  //     throw error;

  //   }))
 return next(req.clone({ setHeaders: headers })).pipe(
      catchError((error: HttpErrorResponse) => {
        console.error('HTTP Error:', error);
        throw error;
      })
    );
  }
      
}