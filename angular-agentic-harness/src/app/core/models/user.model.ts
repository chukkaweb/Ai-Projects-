export interface User {
  id: string;
  email: string;
  displayName: string;
  roles: string[];
}

export interface AuthSession {
  accessToken: string;
  expiresAt: number;
  user: User;
}
