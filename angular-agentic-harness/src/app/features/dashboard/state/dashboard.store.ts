import { DestroyRef, Injectable, computed, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { DashboardService } from '../services/dashboard.service';
import { DashboardSummary } from '../models/dashboard.model';

@Injectable({ providedIn: 'root' })
export class DashboardStore {
  private readonly dashboardService = inject(DashboardService);
  private readonly destroyRef = inject(DestroyRef);

  private readonly summary = signal<DashboardSummary | null>(null);
  private readonly loading = signal(false);
  private readonly error = signal<string | null>(null);

  readonly metrics = computed(() => this.summary()?.metrics ?? []);
  readonly isLoading = this.loading.asReadonly();
  readonly errorMessage = this.error.asReadonly();
  readonly lastUpdated = computed(() => this.summary()?.lastUpdated ?? null);

  constructor() {
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.error.set(null);

    this.dashboardService
      .getSummary()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (data) => {
          this.summary.set(data);
          this.loading.set(false);
        },
        error: () => {
          this.error.set('Unable to load dashboard metrics.');
          this.loading.set(false);
        },
      });
  }
}
