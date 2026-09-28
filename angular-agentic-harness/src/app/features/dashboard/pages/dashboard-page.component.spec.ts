import { ComponentFixture, TestBed } from '@angular/core/testing';
import { signal } from '@angular/core';
import { DashboardPageComponent } from './dashboard-page.component';
import { DashboardStore } from '../state/dashboard.store';
import { DashboardMetric } from '../models/dashboard.model';

describe('DashboardPageComponent', () => {
  let fixture: ComponentFixture<DashboardPageComponent>;

  const metrics = signal<DashboardMetric[]>([
    { id: 'm1', label: 'Users', value: 42, trendPercent: 3.1 },
  ]);

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DashboardPageComponent],
      providers: [
        {
          provide: DashboardStore,
          useValue: {
            metrics: metrics.asReadonly(),
            isLoading: signal(false).asReadonly(),
            errorMessage: signal<string | null>(null).asReadonly(),
            lastUpdated: signal('2026-01-01T00:00:00.000Z').asReadonly(),
          },
        },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(DashboardPageComponent);
    fixture.detectChanges();
  });

  it('renders metric cards from the store', () => {
    const text = (fixture.nativeElement as HTMLElement).textContent ?? '';
    expect(text).toContain('Users');
    expect(text).toContain('42');
  });
});
