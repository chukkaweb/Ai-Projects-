import { TestBed } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { DashboardService } from '../services/dashboard.service';
import { DashboardStore } from './dashboard.store';

describe('DashboardStore', () => {
  it('exposes metrics after load', () => {
    TestBed.configureTestingModule({
      providers: [
        DashboardStore,
        {
          provide: DashboardService,
          useValue: {
            getSummary: () =>
              of({
                lastUpdated: '2026-01-01T00:00:00.000Z',
                metrics: [
                  { id: 'm1', label: 'Users', value: 10, trendPercent: 1 },
                ],
              }),
          },
        },
      ],
    });

    const store = TestBed.inject(DashboardStore);
    expect(store.metrics().length).toBe(1);
    expect(store.isLoading()).toBe(false);
  });

  it('sets error message when load fails', () => {
    TestBed.configureTestingModule({
      providers: [
        DashboardStore,
        {
          provide: DashboardService,
          useValue: {
            getSummary: () => throwError(() => new Error('network')),
          },
        },
      ],
    });

    const store = TestBed.inject(DashboardStore);
    expect(store.errorMessage()).toContain('Unable to load');
  });
});
