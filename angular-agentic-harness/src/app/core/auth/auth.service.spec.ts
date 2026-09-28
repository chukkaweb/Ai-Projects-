import { TestBed } from '@angular/core/testing';
import { AuthService } from './auth.service';

describe('AuthService', () => {
  let service: AuthService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AuthService);
  });

  it('starts unauthenticated', () => {
    expect(service.isAuthenticated()).toBe(false);
    expect(service.getAccessToken()).toBeNull();
  });

  it('exposes token after login and clears on logout', () => {
    service.login(
      { id: '1', email: 'ops@example.com', displayName: 'Ops', roles: ['admin'] },
      'token-123',
    );
    expect(service.isAuthenticated()).toBe(true);
    expect(service.getAccessToken()).toBe('token-123');
    service.logout();
    expect(service.isAuthenticated()).toBe(false);
  });
});
