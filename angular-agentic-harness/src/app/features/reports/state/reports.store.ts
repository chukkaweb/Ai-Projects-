import { DestroyRef, Injectable, inject, signal } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ReportsService } from '../services/reports.service';
import { ReportDefinition } from '../models/report.model';

@Injectable({ providedIn: 'root' })
export class ReportsStore {
  private readonly reportsService = inject(ReportsService);
  private readonly destroyRef = inject(DestroyRef);

  private readonly reports = signal<ReportDefinition[]>([]);
  private readonly loading = signal(false);

  readonly items = this.reports.asReadonly();
  readonly isLoading = this.loading.asReadonly();

  constructor() {
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.reportsService
      .list()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: (items) => {
          this.reports.set(items);
          this.loading.set(false);
        },
        error: () => this.loading.set(false),
      });
  }
}
