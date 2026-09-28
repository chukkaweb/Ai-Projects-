import { TestBed } from '@angular/core/testing';
import { DashboardService } from './dashboard.service';
import { firstValueFrom } from 'rxjs';

describe('DashboardService', () => {
  let service: DashboardService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DashboardService);
  });

  it('returns a summary with metrics', async () => {
    const summary = await firstValueFrom(service.getSummary());
    expect(summary.metrics.length).toBeGreaterThan(0);
    expect(summary.lastUpdated).toBeTruthy();
  });
});
