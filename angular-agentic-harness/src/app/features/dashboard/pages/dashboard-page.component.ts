import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { PageHeaderComponent } from '@shared';
import { MetricCardComponent } from '../components/metric-card.component';
import { DashboardStore } from '../state/dashboard.store';

@Component({
  selector: 'app-dashboard-page',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [PageHeaderComponent, MetricCardComponent],
  template: `
    <app-page-header
      title="Dashboard"
      subtitle="Operational snapshot for the current workspace."
    />

    @if (store.isLoading()) {
      <p data-testid="dashboard-loading">Loading metrics…</p>
    } @else if (store.errorMessage()) {
      <p class="error" data-testid="dashboard-error">{{ store.errorMessage() }}</p>
    } @else {
      <section class="metrics" data-testid="dashboard-metrics">
        @for (metric of store.metrics(); track metric.id) {
          <app-metric-card [metric]="metric" />
        }
      </section>
      @if (store.lastUpdated(); as updated) {
        <p class="meta">Last updated: {{ updated }}</p>
      }
    }
  `,
  styles: `
    .metrics {
      display: grid;
      gap: 1rem;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    }

    .error {
      color: #b42318;
    }

    .meta {
      margin-top: 1rem;
      color: #5c6570;
      font-size: 0.875rem;
    }
  `,
})
export class DashboardPageComponent {
  readonly store = inject(DashboardStore);
}
