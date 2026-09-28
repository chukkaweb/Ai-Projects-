import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';

/**
 * Normalizes HTTP failures for feature stores/services.
 * Does not surface raw payloads to the UI — callers map to safe messages.
 */
export const errorInterceptor: HttpInterceptorFn = (req, next) =>
  next(req).pipe(
    catchError((error: unknown) => {
      if (error instanceof HttpErrorResponse) {
        const message =
          error.status === 0
            ? 'Network error — check connectivity or API base URL.'
            : `Request failed (${error.status}).`;
        return throwError(() => new Error(message));
      }
      return throwError(() => error);
    }),
  );
