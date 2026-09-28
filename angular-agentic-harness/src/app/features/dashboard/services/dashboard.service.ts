import { Injectable, signal } from '@angular/core';
import { Observable, of, tap } from 'rxjs';
import { DashboardSummary } from '../models/dashboard.model';

@Injectable({ providedIn: 'root' })
export class DashboardService {
  private readonly cache = signal<DashboardSummary | null>(null);

  getSummary(): Observable<DashboardSummary> {
    const cached = this.cache();
    if (cached) {
      return of(cached);
    }

    const summary: DashboardSummary = {
      lastUpdated: new Date().toISOString(),
      metrics: [
        { id: 'active-users', label: 'Active users', value: 1284, trendPercent: 4.2 },
        { id: 'open-tickets', label: 'Open tickets', value: 37, trendPercent: -8.1 },
        { id: 'revenue', label: 'Revenue (k)', value: 92, trendPercent: 2.6 },
      ],
    };

    return of(summary).pipe(tap((data) => this.cache.set(data)));
  }
}
