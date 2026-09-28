import { TestBed } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { ReportsService } from '../services/reports.service';
import { ReportsStore } from './reports.store';

describe('ReportsStore', () => {
  it('loads report items', () => {
    TestBed.configureTestingModule({
      providers: [
        ReportsStore,
        {
          provide: ReportsService,
          useValue: {
            list: () =>
              of([
                {
                  id: 'r1',
                  name: 'Usage',
                  description: 'Daily',
                  cadence: 'daily' as const,
                },
              ]),
          },
        },
      ],
    });

    const store = TestBed.inject(ReportsStore);
    expect(store.items().length).toBe(1);
    expect(store.isLoading()).toBe(false);
  });

  it('clears loading on error', () => {
    TestBed.configureTestingModule({
      providers: [
        ReportsStore,
        {
          provide: ReportsService,
          useValue: {
            list: () => throwError(() => new Error('boom')),
          },
        },
      ],
    });

    const store = TestBed.inject(ReportsStore);
    expect(store.isLoading()).toBe(false);
    expect(store.items().length).toBe(0);
  });
});
