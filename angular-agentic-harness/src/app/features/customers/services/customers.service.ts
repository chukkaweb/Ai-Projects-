import { Injectable, signal } from '@angular/core';
import { Observable, of, tap } from 'rxjs';
import { Customer } from '../models/customer.model';

const SEED: Customer[] = [
  {
    id: 'c-1001',
    name: 'Acme Robotics',
    email: 'ops@acmerobotics.example',
    status: 'active',
    createdAt: '2026-01-12T10:00:00.000Z',
  },
  {
    id: 'c-1002',
    name: 'Northwind Labs',
    email: 'hello@northwind.example',
    status: 'prospect',
    createdAt: '2026-03-04T14:30:00.000Z',
  },
  {
    id: 'c-1003',
    name: 'Contour Analytics',
    email: 'team@contour.example',
    status: 'inactive',
    createdAt: '2025-11-21T09:15:00.000Z',
  },
];

@Injectable({ providedIn: 'root' })
export class CustomersService {
  private readonly cache = signal<Customer[] | null>(null);

  list(): Observable<Customer[]> {
    const cached = this.cache();
    if (cached) {
      return of(cached);
    }
    return of(SEED).pipe(tap((customers) => this.cache.set(customers)));
  }
}
