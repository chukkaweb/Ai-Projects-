import { Injectable, signal, computed } from '@angular/core';
import { AuthSession, User } from '../models';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly session = signal<AuthSession | null>(null);

  readonly user = computed(() => this.session()?.user ?? null);
  readonly isAuthenticated = computed(() => !!this.session()?.accessToken);

  login(user: User, accessToken: string, expiresInMs = 3_600_000): void {
    this.session.set({
      user,
      accessToken,
      expiresAt: Date.now() + expiresInMs,
    });
  }

  logout(): void {
    this.session.set(null);
  }

  getAccessToken(): string | null {
    const current = this.session();
    if (!current) {
      return null;
    }
    if (Date.now() >= current.expiresAt) {
      this.logout();
      return null;
    }
    return current.accessToken;
  }
}
