import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { PageHeaderComponent } from '@shared';
import { ReportCardComponent } from '../components/report-card.component';
import { ReportsStore } from '../state/reports.store';

@Component({
  selector: 'app-reports-page',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [PageHeaderComponent, ReportCardComponent],
  template: `
    <app-page-header
      title="Reports"
      subtitle="Scheduled insights available to this workspace."
    />

    @if (store.isLoading()) {
      <p data-testid="reports-loading">Loading reports…</p>
    } @else {
      <section class="grid" data-testid="reports-grid">
        @for (report of store.items(); track report.id) {
          <app-report-card [report]="report" />
        }
      </section>
    }
  `,
  styles: `
    .grid {
      display: grid;
      gap: 1rem;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    }
  `,
})
export class ReportsPageComponent {
  readonly store = inject(ReportsStore);
}
