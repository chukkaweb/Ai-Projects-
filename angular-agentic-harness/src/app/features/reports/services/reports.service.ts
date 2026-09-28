import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { ReportDefinition } from '../models/report.model';

@Injectable({ providedIn: 'root' })
export class ReportsService {
  list(): Observable<ReportDefinition[]> {
    return of([
      {
        id: 'r-usage',
        name: 'Usage summary',
        description: 'Daily active usage by workspace.',
        cadence: 'daily',
      },
      {
        id: 'r-churn',
        name: 'Churn risk',
        description: 'Accounts with declining engagement.',
        cadence: 'weekly',
      },
      {
        id: 'r-revenue',
        name: 'Revenue rollup',
        description: 'Booked and recognized revenue by segment.',
        cadence: 'monthly',
      },
    ]);
  }
}
