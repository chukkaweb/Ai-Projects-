import { TestBed } from '@angular/core/testing';
import { HttpRequest, HttpResponse } from '@angular/common/http';
import { of } from 'rxjs';
import { authInterceptor } from './auth.interceptor';
import { AuthService } from '../auth/auth.service';

describe('authInterceptor', () => {
  it('attaches Authorization when a token exists', () => {
    TestBed.configureTestingModule({});
    const auth = TestBed.inject(AuthService);
    auth.login(
      { id: '1', email: 'ops@example.com', displayName: 'Ops', roles: [] },
      'abc',
    );

    const req = new HttpRequest('GET', '/api/ping');
    const next = (request: HttpRequest<unknown>) => {
      expect(request.headers.get('Authorization')).toBe('Bearer abc');
      return of(new HttpResponse({ status: 200 }));
    };

    TestBed.runInInjectionContext(() => {
      authInterceptor(req, next).subscribe();
    });
  });
});
