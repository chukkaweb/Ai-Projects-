import { TestBed } from '@angular/core/testing';
import { firstValueFrom } from 'rxjs';
import { ReportsService } from './reports.service';

describe('ReportsService', () => {
  it('lists report definitions', async () => {
    TestBed.configureTestingModule({});
    const service = TestBed.inject(ReportsService);
    const reports = await firstValueFrom(service.list());
    expect(reports.length).toBeGreaterThan(0);
    expect(reports[0].cadence).toBeTruthy();
  });
});
